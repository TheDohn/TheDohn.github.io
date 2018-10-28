import pandas as pd

def head_with_full_columns(pd_in, row_amount = 5):
    """Returns all columns and row_amount of rows. Useful for scanning large amounts of features."""
    with pd.option_context('display.max_columns', len(pd_in.iloc[0])):
        display(pd_in[:row_amount])

def balanced_sample(df_in, total_size, rand_state):
    """Returns a balanced sample as a Pandas Dataframe."""
    s0 = df_in[df_in['TARGET']==0].sample(n = total_size//2, random_state = rand_state)
    s1 = df_in[df_in['TARGET']==1].sample(n = total_size//2, random_state = rand_state)
    new_df = pd.concat([s0,s1])
    new_df.sort_index(inplace = True)
    return new_df

def get_sub_frame(df_in, cond_dict):
    """Returns the sub frame for which the conditions cond_dict hold True. """
    curr_keys = cond_dict.keys()
    
    df_curr = df_in
    for key in curr_keys:
        df_curr = df_curr[df_curr[key]==cond_dict[key]]
    return df_curr
  

def my_over_sample(row_integers_list_to_balance, df_in, feature_to_balance_on='TARGET', ret='row_integers_list'):
    """Parameters: row_integers_list_to_balance: list or numpy array
                        list of indices we are balancing  
                
                    df_in : Pandas Dataframe
                        Pandas Dataframe to be oversampled.
                        
                    feature_to_balance_on: string
                        Rebalance df by oversampling this feature.
                        
                    ret: string
                        'Dataframe' or 'indices'. Pick which to return. 
      
        Returns: final_indices_list: list
        
                     Balanced indices, with indices altered by fractional values to denote additional samples.
      
        NOTES:
            -This only works on binary features, ordering more than that will require much more work."""

    # values of feature
    feat_vals = df_in[feature_to_balance_on].value_counts().index
    if len(feat_vals)!=2:
        raise ValueError('df_in feature does not have 2 values.')

    sub_df_feat_vals = df_in.iloc[row_integers_list_to_balance,:][feature_to_balance_on].value_counts().index    
    if len(sub_df_feat_vals)!=2:
        raise ValueError('For df_in for indices passed, feature does not have 2 values.')
        
    # look at the sub-df we want to balance    
    sub_df_to_balance  = df_in.iloc[row_integers_list_to_balance,:][[feature_to_balance_on]]
                
    # over- and under-represented entries in df
    over_repd_df = sub_df_to_balance[sub_df_to_balance[feature_to_balance_on] == feat_vals[0]]
    under_repd_df = sub_df_to_balance[sub_df_to_balance[feature_to_balance_on] == feat_vals[1]]
    
    # indices in ORGINIAL df that are over and under-represented
    # Scanning through entire df is likely inefficient, but I don't see another way. 
    over_repd_indices = [df_in.index.get_loc(x) for x in over_repd_df.index.values]
    under_repd_indices = [df_in.index.get_loc(x) for x in under_repd_df.index.values]
    
    # how many times to oversampled the under-sampled indices
    quotient, remainder = divmod(len(over_repd_indices), len(under_repd_indices))
        
    if quotient == 1 and remainder==0:
        print('This df was already balanced!')            
        
    # create indices list by oversampling under-repd indices
    # NOTE THAT when the remainder above is nonzero some under-sampled indices are repd an unequal amount of times
    final_indices_list = over_repd_indices + quotient*under_repd_indices + under_repd_indices[:remainder]
    
    return final_indices_list
    
    
    
   
def rebalance_sklearns_training_KFolds(df_in, sklearns_KFolds_split_output, feature_to_balance_on='TARGET'):
    """Parameters: df_in: Pandas Dataframe
                       input Dataframe
                        
                   StratifiedKFold_split_output: enumerator or list
                       unbalanced output from StratifiedKFold.split()
                       
        Returns: Balanced training indices (validation untouched) as formatted from StratifiedKFold.split(). """
    
    return [  ( my_over_sample(f[0], df_in, feature_to_balance_on), list(f[1]) )  for f in sklearns_KFolds_split_output]

