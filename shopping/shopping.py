import csv
import sys
import numpy as np
import pandas as pd

from sklearn.linear_model import Perceptron
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def get_model(model_name):
    switcher = {
        'KNN': KNeighborsClassifier(n_neighbors=1),
        'Perceptron': Perceptron(),
        'SVM': svm.SVC(),
        'GaussianNB': GaussianNB(),
    }
    return switcher.get(model_name, None)


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    MODEL_NAME = ['KNN', 'Perceptron', 'SVM', 'GaussianNB']
    for model_name in MODEL_NAME:
        print(model_name)
        # Train model and make predictions
        model = train_model(X_train, y_train, model_name)
        predictions = model.predict(X_test)
        sensitivity, specificity = evaluate(y_test, predictions)

        correct = 0
        incorrect = 0
        total = 0
        for actual, predicted in zip(y_test, predictions):
            total += 1
            if actual == predicted:
                correct += 1
            else:
                incorrect += 1

        # Print results
        print(f"Results for model {type(model).__name__}")
        print(f"Correct: {correct}")
        print(f"Incorrect: {incorrect}")
        print(f"Accuracy: {100 * correct / total:.2f}%")
        print(f"True Positive Rate: {100 * sensitivity:.2f}%")
        print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    df = pd.read_csv(filename)
    # Show raw data from csv file
    '''
                Administrative  Administrative_Duration  Informational  Informational_Duration  ProductRelated 
    0               0                      0.0              0                     0.0               1 
    1               0                      0.0              0                     0.0               2
    2               0                      0.0              0                     0.0               1 
    3               0                      0.0              0                     0.0               2 
    '''
    # print(df.head(5))

    # Check null value
    # print(df.isnull().any())

    # Print different value in one column
    # print(df.Month.unique())
    # Month should be 0 for January, 1 for February, 2 for March, etc. up to 11 for December.
    month_map = {'JAN': 0, 'FEB': 1, 'MAR': 2, 'APR': 3, 'MAY': 4, 'JUNE': 5, 'JUL': 6, 'AUG': 7, 'SEP': 8, 'OCT': 9,
                 'NOV': 10, 'DEC': 11}
    # Avoid different cases
    df.Month = df.Month.str.upper().map(month_map)

    # VisitorType should be 1 for returning visitors and 0 for non-returning visitors.
    # df.VisitorType = df.VisitorType.replace({'Returning_Visitor': 1, 'New_Visitor': 0})
    df.VisitorType = np.where(df.VisitorType == 'Returning_Visitor', 1, 0)

    # Weekend should be 1 if the user visited on a weekend and 0 otherwise.
    df.Weekend = df.Weekend.replace({True: 1, False: 0})

    # Each value of labels should either be the integer 1, if the user did go through with a purchase, or 0 otherwise.
    df.Revenue = df.Revenue.replace({True: 1, False: 0})

    '''
        Administrative  Administrative_Duration  Informational  Informational_Duration  ProductRelated  ProductRelated_Duration  ...  Browser  Region  TrafficType  VisitorType  Weekend  Revenue
    0               0                      0.0              0                     0.0               1                 0.000000  ...        1       1            1            1        0        0
    1               0                      0.0              0                     0.0               2                64.000000  ...        2       1            2            1        0        0
    2               0                      0.0              0                     0.0               1                 0.000000  ...        1       9            3            1        0        0
    3               0                      0.0              0                     0.0               2                 2.666667  ...        2       2            4            1        0        0
    4               0                      0.0              0                     0.0              10               627.500000  ...        3       1            4            1        1        0
    '''
    # print(df.head(5))

    # Check if they have null value
    # print(df.isnull().any())

    '''
    The load_data function should accept a CSV filename as its argument, open that file, and return a tuple (evidence, labels). 
    evidence should be a list of all of the evidence for each of the data points, and labels should be a list of all of the labels for each data point.
    '''
    evidence = df.iloc[:, 0:-1].copy().values.tolist()  # To avoid the case where changing evidence also changes df
    labels = df.iloc[:, -1:].copy().values.tolist()  # To avoid the case where changing label also changes df

    '''
    [0, 0.0, 0, 0.0, 2, 64.0, 0.0, 0.1, 0.0, 0.0, 1.0, 2, 2, 1, 2, 1, 0]
    [0]
    '''
    # print(evidence[1])
    # print(labels[1])

    # Create a tuple
    result = (evidence, labels)

    return result


def train_model(evidence, labels, model_name):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = get_model(model_name)
    model = model.fit(evidence, labels)
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    # Compute how well we performed TP TN FP FN TT TF
    def check_preform(labels, predictions):
        TP = 0
        TN = 0
        FP = 0
        FN = 0
        for i in range(len(labels)):
            if (predictions[i] == labels[i][0] == 1):
                TP += 1
            elif (predictions[i] != labels[i][0] == 0):
                FP += 1
            elif (predictions[i] == labels[i][0] == 0):
                TN += 1
            else:
                FN += 1
        return TP, TN, FP, FN,

    (TP, TN, FP, FN) = check_preform(labels, predictions)
    # print all values
    # print("TP" + str(TP))
    # print("TN" + str(TN))
    # print("FP" + str(FP))
    # print("FN" + str(FN))
    # sensitivity
    sensitivity = TP / (TP + FN)

    # specificity
    specificity = TN / (TN + FP)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
