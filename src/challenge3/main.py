
from argparse import ArgumentParser
from functools import partial
from pathos.multiprocessing import ThreadingPool as Pool

def printCombined(pool, resolved):
    """
    :param pool: thread pool
    :param resolved: list of resolved partitions
    :return: none
    """

    def _printCombined(fixed, next):
        """
        :param fixed: the fixed part of the string
        :param next: the remaining resolved substrings
        :return: a list of waiters for all strings
        """
        if len(next) == 0:
            print(fixed)
            return
        next_methods = list(map(lambda chunk: fixed + chunk, next[0]))
        return [pool.apipe(partial(_printCombined, next=next[1:]), next_method) for next_method in next_methods]

    tasks = [_printCombined("", resolved)]
    while len(tasks) > 0:
        task = tasks.extend(filter(lambda l: l, map(lambda l: l.get(), tasks.pop())))

def resolveVariables(sub_str: str):
    """
    :param sub_str: the substring that variables need to be resolved for
    :return: a list of the possible variable patterns
    """
    resolved = [""]
    for s in sub_str:
        if s == '1' or s=='0':
            resolved = list(map(lambda r: r+s, resolved))
        elif s == 'X':
            temp = list(map(lambda r: r+'1', resolved))
            resolved = list(map(lambda r: r+'0', resolved))
            resolved.extend(temp)
        else:
            raise Exception("Key Not Allowed: %s" % s)
    return resolved

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Challenge #3",
        description="Print all combinations of the given string"
    )

    parser.add_argument(
        "input_string",
        help="the string to be randomized"
    )

    parser.add_argument(
        "--partition_size",
        help="the size of partitions to be used",
        type=int,
        default=1
    )

    parser.add_argument(
        "--max_threads",
        help="the max number of threads to use",
        type=int,
        default=1
    )

    args = vars(parser.parse_args())

    pool = Pool(args["max_threads"])
    partitions = [args['input_string'][i:i+args['partition_size']] for i in range(0,len(args['input_string']),args['partition_size'])]
    partitionsm = pool.map(resolveVariables, partitions)

    printCombined(pool, partitionsm)