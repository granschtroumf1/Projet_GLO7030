from numpy.random import permutation
from sklearn import svm, datasets

from sacred import Experiment

from sacred.observers import FileStorageObserver


ex = Experiment('iris_rbf_svm')
ex.observers.append(FileStorageObserver.create('my_runs'))


@ex.config
def cfg():
  C = 1.4
  gamma = 0.6

@ex.automain
def run(C, gamma):
  iris = datasets.load_iris()
  per = permutation(iris.target.size)
  iris.data = iris.data[per]
  iris.target = iris.target[per]

  print("bonjour")

  clf = svm.SVC(C, 'rbf', gamma=gamma)
  clf.fit(iris.data[:90],
          iris.target[:90])

  print("epoch numero 3")
  return clf.score(iris.data[90:],
                   iris.target[90:])