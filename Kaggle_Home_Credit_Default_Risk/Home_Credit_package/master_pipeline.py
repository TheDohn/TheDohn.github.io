
from sklearn.base import BaseEstimator, TransformerMixin

from sklearn.preprocessing import StandardScaler, PolynomialFeatures

from sklearn.pipeline import make_pipeline, FeatureUnion, Pipeline

# pre sklearn v20 stuff: https://github.com/scikit-learn/scikit-learn/tree/5fcf6f486fb0134c91f5a8741fe7e450539883f0/sklearn/preprocessing
from Home_Credit_package.sklearn_future import CategoricalEncoder 

import numpy as np

#from sklearn.linear_model import LogisticRegression


class ItemSelector(BaseEstimator, TransformerMixin):
    """For data grouped by feature, select subset of data at a provided key.

    The data is expected to be stored in a 2D data structure, where the first
    index is over features and the second is over samples.  i.e.

    >> len(data[key]) == n_samples

    Please note that this is the opposite convention to scikit-learn feature
    matrixes (where the first index corresponds to sample).

    ItemSelector only requires that the collection implement getitem
    (data[key]).  Examples include: a dict of lists, 2D numpy array, Pandas
    DataFrame, numpy record array, etc.

    >> data = {'a': [1, 5, 2, 5, 2, 8],
               'b': [9, 4, 1, 4, 1, 3]}
    >> ds = ItemSelector(key='a')
    >> data['a'] == ds.transform(data)

    ItemSelector is not designed to handle data grouped by sample.  (e.g. a
    list of dicts).  If your data is structured this way, consider a
    transformer along the lines of `sklearn.feature_extraction.DictVectorizer`.

    Parameters
    ----------
    key : hashable, required
        The key corresponding to the desired value in a mappable.
    """
    def __init__(self, key):
        self.key = key

    def fit(self, x, y=None): # y are the targets, I believe. This really is the fit function from sklearn.
        return self

    def transform(self, data_dict):
        return data_dict[self.key]
    
class IntermediateReshape(BaseEstimator, TransformerMixin):
    """This just format the reshape function for a 1-D array from a single feature
    as a class to be called in pipeline in between 
    LabelEncoder (which outputs an array [1,2,3,4,...]) 
    and OneHotEncoder (which takes the same array as [[1],[2],[3],[4],...])."""
    def __init__(self): # I don't think this is technically necessary here, so I drop it. 
        self

    def fit(self, x, y = None): # y are the targets, I believe. This really is the fit function from sklearn.
        return self

    def transform(self, x):
        return np.array(x).reshape(len(x),1)

    
def create_poly_labels(f_list, p_list):
    if sum(p_list)==0:
        return 'poly_deg=0'
    
    else:
        fp_list = tuple([(f, p) for f,p in zip(f_list, p_list) if p !=0])#[f + '^'+ str(p) for f,p in zip(f_list, p_list) if p !=0]
        return fp_list#"_".join(fp_list)    
    
# for getting full list of features down to categories, polynomial powers etc. 
# this is a bit of hack since many sklearn classes have a 'get_feature_names()' attribute
# BUT some do not, and changing those things would require some digging, 
# so easier to write something that does what I need for now. 
def get_key_or_poly_feat_from_pipeline(pipeline_in, intx_f_list, pwr_array):
       
    pipe_name_pieces = pipeline_in[0].split('_')
    # all but the last 2 pieces are the name
    feature = "_".join(pipe_name_pieces[:-2])
    # grab last portion of pipeline label, which is cat or poly by MY convention
    cat_or_poly = pipe_name_pieces[-1]
    
    # return the relevant named steps
    if cat_or_poly == 'categoricalencoder':
        cat_list = pipeline_in[1].named_steps['categoricalencoder'].categories_[0]
        return [(feature, i) for i in cat_list ]
    
    if cat_or_poly == 'polynomialfeatures':
        poly_list = pipeline_in[1].named_steps['polynomialfeatures'].powers_
        # flatten this list
        poly_list = [x[0] for x in poly_list]
        return [(feature, i) for i in poly_list]
    
    if cat_or_poly == 'polynomialiteractions':
        return [create_poly_labels(intx_f_list, p_list) for p_list in pwr_array]
    
def get_all_feature_names_from_pipeline(transformation_list_in, intx_f_list, pwr_array):
    """Returns list of categorical and polynomial features if following my named steps convention."""
    # the full list and flatten it. 
    full_list = [get_key_or_poly_feat_from_pipeline(t, intx_f_list, pwr_array) for t in transformation_list_in]
    #return [x for y in full_list for x in y] Seems better to just make a giant string
    return [str(x) for y in full_list for x in y]


def master_pipeline(df_in, int_cutoff, poly_deg, feats_with_interaction = []):
    """Arguments:   df_in:input dataframe
                    int_cutoff: division between continuous and discrete numerical features
                    poly_deg: degree to fit polynomials
                    feats_with_interaction: features to include interactions up to poly_deg
                    
        Outputs:    df_trans: pipelined dataframe
                    all_piped_feature_names: list of final pipeline features names, including polynomial inteaction degree
                    full_pipeline: the pipeline itself
                    total_transform_list
    """
    # remove 'TARGET' values in case I have not already
    feats = list(df_in.columns)
    
    if 'TARGET' in feats:
        feats.remove('TARGET')
             
    feats_wo_intx = [f for f in feats if f not in feats_with_interaction]

    int_list = list(df_in[feats_wo_intx].select_dtypes('int64'))
    cats_feats = list(df_in[feats_wo_intx].select_dtypes('object')) + list(df_in[feats_wo_intx].select_dtypes('bool'))
    floats_feats = list(df_in[feats_wo_intx].select_dtypes('float64'))
    
    # do rough splitting of integer features into ones that are really catagorical (few #s), and ones that are continuous (many #s)
    continuous_ints_feats = [x for x in int_list if int_cutoff <= len(np.unique(df_in[x]))]
    categorical_ints_feats = [x for x in int_list if int_cutoff > len(np.unique(df_in[x]))]
 
    # check all features are accounted for
    print('Total original feat len is '+ str(len(feats)) +'.', 'Sum of feats is ' + str(len(cats_feats) + len(floats_feats) +\
    len(int_list) + len(feats_with_interaction)) +'.' )
    
    if len(feats) !=len(cats_feats) + len(floats_feats) + len(int_list) + len(feats_with_interaction) :
        raise ValueError('Number of features does not match size of input Dataframe.')

    # construct all feature pipelines by dtype
    cat_transform_list = [(f +'_pipe_categoricalencoder', 
                               make_pipeline(
                                        ItemSelector(key = f), 
                                        IntermediateReshape(), 
                                        CategoricalEncoder(encoding='onehot',handle_unknown='ignore') ) ) 
                           for f in cats_feats ]

    float_transform_list = [(f +'_pipe_polynomialfeatures', 
                                 make_pipeline(
                                             ItemSelector(key = f), 
                                             IntermediateReshape(),
                                             PolynomialFeatures(degree = poly_deg),
                                             StandardScaler())) 
                            for f in floats_feats ]

    cat_int_transform_list = [(f +'_pipe_categoricalencoder',
                                    make_pipeline(
                                            ItemSelector(key = f), 
                                           IntermediateReshape(), 
                                           CategoricalEncoder(encoding='onehot',handle_unknown='ignore')  )) 
                              for f in categorical_ints_feats ]

    continuous_int_transform_list = [(f +'_pipe_polynomialfeatures', 
                                          make_pipeline(
                                                  ItemSelector(key = f), 
                                                  IntermediateReshape(), 
                                                  PolynomialFeatures(degree = poly_deg), 
                                                  StandardScaler())) 
                                     for f in continuous_ints_feats]
    
    
    total_transform_list = cat_transform_list + float_transform_list + cat_int_transform_list + continuous_int_transform_list 

    # if there are interactions, make those pipelines along with non-interaction terms for those features
    if feats_with_interaction:
        
        polynomial_interactions = [('allfeats_pipe_polynomialiteractions',
                                        make_pipeline(
                                                ItemSelector(key = feats_with_interaction),
                                                PolynomialFeatures(degree = poly_deg, interaction_only=False), 
                                                StandardScaler() ) )
                              ]
        total_transform_list = total_transform_list + polynomial_interactions
    
    # contruct the full pipieline and fit it
    full_pipeline = FeatureUnion(total_transform_list)
    df_trans = full_pipeline.fit_transform(df_in)
    
    # get all the names for the pipelined features
    all_piped_feature_names = get_all_feature_names_from_pipeline(total_transform_list,
                                                                  feats_with_interaction,
                                                                  # this relies on the last transformer being the poly intxs, if it exists. 
                                                                  total_transform_list[-1][1].named_steps['polynomialfeatures'].powers_)
    
    # check that final pipelined data has the correct size for all final features
    print('Final array is length '+ str(df_trans.shape[1])+'.' , 'final feature list is length '  +str(len(all_piped_feature_names))+'.' )
    if df_trans.shape[1] != len(all_piped_feature_names) :
        raise ValueError('Final number of features does not match size of pipelined Dataframe.')

    return df_trans, all_piped_feature_names, full_pipeline, total_transform_list

