import numpy as np
import torch.nn as nn

from torch.autograd import Variable
#inspiré de :
#https://github.com/benhamner/Metrics/tree/master/Python/ml_metrics
def apk(actual, predicted, k=3):
    """

    Pour un seul

    Computes the average precision at k.
    This function computes the average prescision at k between two lists of
    items.
    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The average precision at k over the input lists
    """
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k=3):
    """
    Computes the mean average precision at k.
    This function computes the mean average prescision at k between two lists
    of lists of items.
    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted
             (order doesn't matter in the lists)
             plutot une list d'integer


    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements
    Returns
    -------
    score : double
            The mean average precision at k over the input lists
    """

    actual=[[value] for value in actual]

    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])




def calcul_metric_concours(model, val_loader, use_gpu=True):
    model.train(False)
    true = []
    pred = []
    val_loss = []
    pred_top3=[]

    criterion = nn.CrossEntropyLoss()
    model.eval()

    for j, batch in enumerate(val_loader):

        inputs, targets = batch
        if use_gpu:
            inputs = inputs.cuda()
            targets = targets.cuda()

        inputs = Variable(inputs, volatile=True)
        targets = Variable(targets, volatile=True)
        output = model(inputs)

        predictions = output.max(dim=1)[1]
        predictions_top_3 = output.topk(3)[1]

        val_loss.append(criterion(output, targets).item())
        true.extend(targets.data.cpu().numpy().tolist())
        pred.extend(predictions.data.cpu().numpy().tolist())
        pred_top3.extend(predictions_top_3.data.cpu().numpy().tolist())


    top3_score=mapk(true,pred_top3)
    print(top3_score)

    model.train(True)
    pass