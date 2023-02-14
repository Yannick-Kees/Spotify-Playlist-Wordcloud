import sys

def report_progress(current, total):
    # Prints out, how far the training process is

    # Parameters:
    #     current:    where we are right now
    #     total:      how much to go
    #     error:      Current Error, i.e. evaluation of the loss functional

    sys.stdout.write('\rProgress: {:.2%}'.format(float(current)/total))

    if current==total:
        sys.stdout.write('\n')
        
    sys.stdout.flush()