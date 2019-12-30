def MergeModel(model1:dict,model2:dict)->dict:
    for key in model1:
        if key in model2:
            model2[key]=(model1[key]+model2[key])/2
        else:
            model2[key]=model1[key]
    return model2