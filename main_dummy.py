from datasets import EditDataSet
from datasets import EditVocab
import os

def dataset_example():
    import pdb
    pdb.set_trace()
    # dset = EditDataSet(False, False, False)
    print "\n\nPrinting info about the dataset"
    train_data = EditDataSet.from_file(os.path.join('.data', 'Reinflection', 'kat.V', 'kat.V.form.dev.txt'), EditVocab())
    print "train_data.vocab = {}".format(train_data.vocab)
    print "train_data.training_data = {}".format(train_data.training_data)
    print "train_data.length = {}".format(train_data.length)
    print "train_data.filename = {}".format(train_data.filename)
    print "type(train_data.samples) = {}".format(type(train_data.samples))
    print "train_data.samples[5] = {}".format(train_data.samples[5])
    print "train_data.tag_wraps = {}".format(train_data.tag_wraps)
    print "train_data.verbose = {}".format(train_data.verbose)


if __name__ == '__main__':
    dataset_example()