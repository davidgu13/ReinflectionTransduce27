import os
import codecs

from defaults import EVALM_PATH

def write_stats_file(dev_accuracy, paths, data_arguments, model_arguments, optim_arguments):

    with open(paths['stats_file_path'], 'w') as w:
        
        print >> w, 'LANGUAGE: {}, REGIME: {}'.format(paths['lang'], paths['regime'])
        print >> w, 'Train path:   {}'.format(paths['train_path'])
        print >> w, 'Dev path:     {}'.format(paths['dev_path'])
        print >> w, 'Test path:    {}'.format(paths['test_path'])
        print >> w, 'Results path: {}'.format(paths['results_file_path'])
        
        for k, v in paths.iteritems():
            if k not in ('lang', 'regime', 'train_path', 'dev_path',
                         'test_path', 'results_file_path'):
                print >> w, '{:20} = {}'.format(k, v)
        print >> w
        
        for name, args in (('DATA ARGS:', data_arguments),
                           ('MODEL ARGS:', model_arguments),
                           ('OPTIMIZATION ARGS:', optim_arguments)):
            print >> w, name
            for k, v in args.iteritems():
                print >> w, '{:20} = {}'.format(k, v)
            print >> w
       
        print >> w, 'DEV ACCURACY (internal evaluation) = {}'.format(dev_accuracy)


def external_eval(output_path, gold_path, batches, predictions, sigm2017format, evalm_path=EVALM_PATH):

    pred_path = output_path + 'predictions'
    # eval_path = output_path + 'eval'
    
    # if sigm2017format is True:
    #     line = u'{LEM}\t{PRE}\t{FET}\n'
    #     format_flag = ''
    #     merge_keys_flag = '--merge_same_keys'
    # else:
    #     line = u'{LEM}\t{FET}\t{PRE}\n'
    #     format_flag = '--format2016'
    #     merge_keys_flag = ''

    # line = u'{INP}\t{IFET}\t{OUT}\t{OFET}\n'
    # line = u'{IN}\t{IFET}\t{WORD}\t{FET}\n'
    line = u'{IFET}\t{IN}\t{FET}\t{WORD}\t{GOLD}\n'

    # WRITE FILE WITH PREDICTIONS
    with codecs.open(pred_path, 'w', encoding='utf8') as w:
        for sample, prediction in zip((s for b in batches for s in b), predictions):
            # w.write(line.format(LEM=sample.lemma_str, PRE=prediction, FET=sample.feat_str))
            # w.write(line.format(IN=sample.samples[0].lemma_str, IFET=sample.samples[0].in_feat_str, WORD=prediction, FET=sample.out_feat_str))
            w.write(line.format(IN=sample.lemma_str, IFET=sample.in_feat_str, WORD=prediction, FET=sample.out_feat_str, GOLD=sample.word_str))

    # CALL EXTERNAL EVAL SCRIPT
    # os.system('python {} --gold {} --guesses {} {} {} | tee {}'.format(
    #         evalm_path, gold_path, pred_path, format_flag, merge_keys_flag, eval_path))