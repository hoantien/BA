def describe_statistic(data):
    data_statistic = data.describe()
    
    # Describe the dataset
    data_statistic = data_statistic.describe()
    data_statistic.insert(0,"Statistics",["count","mean","min","25%","50%","75%","max","std"])
    
    return data_statistic