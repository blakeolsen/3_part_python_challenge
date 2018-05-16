
from argparse import ArgumentParser
from functools import reduce
from math import pow, ceil
from pathos.multiprocessing import ThreadingPool as Pool
from re import match

def parse_line(exp):
    """
    parse each line of the file
    :param line: the line of the file
    :return: index, item, price
    """
    index, line = exp
    try:
        m = match("^([\s\S]+),\s*(\d+)", str(line))
        return {
            'index': index,
            'item': m.group(1).replace("b'", ""),
            'price': int(m.group(2))
        }
    except:
        raise Exception('could not parse expression: %s' % line)

def append_or_none(l: list, i):
    return l+[i] if l else None

def subset_sum(total_money: int, all_items: list, total_gifts: int, thread_pool, partitions:int=1):
    """
    :param total_money: total value of the gift card
    :param all_items: all possible gifts
    :param total_gifts: number of gifts to be purchased
    :param partitions: number of partitions the available items gets split into
    :return: the list of items with the least sum
    """
    myrounds = 0
    def _subset_sum(start: int, remaining_money: int, remaining_gifts: int):
        """
        :param start: lower bound index
        :param remaining_money: amount of money remaining
        :param remaining_gifts: list of gifts already purchased
        :return: {leftover, gift_list}
        """
        if remaining_money < 0: # all money has been spent
            return [None]
        elif start > len(all_items): # at the end of the list
            return [None]
        elif remaining_gifts <= 0: # all gifts have been gathered
            return [remaining_money]
        else: # try combinations of new gifts to add
            most_efficient = [None]
            spacing = int(ceil((len(all_items) - start) / partitions))

            while spacing > 0 and start < len(all_items):
                # sample the is evenly to split list to avoid going through entire list
                batch = list(range(len(all_items)))[start:len(all_items):spacing]

                # fetch results of additional gifts
                results = list(
                    thread_pool.map(
                        lambda item: _subset_sum(
                            start=item+1, # the next round includes all items after the current one
                            remaining_money=remaining_money - all_items[item]['price'], # subtract the cost of this item
                            remaining_gifts=remaining_gifts-1 # subtract number of gifts needed
                        ) + [item], # add the item to the items list with backwards recursion
                        batch
                    ),
                )

                temp = list(filter(lambda item: item[0] != None, results)) # remove all null results
                if len(temp) == 0:
                    return most_efficient # none of the new partition solutions work
                most_efficient_partition = min(temp, key=lambda item: item[0]) # find the most efficient solution of the partition

                if (most_efficient[0] != None) and (most_efficient[0] < most_efficient_partition[0]):
                    return most_efficient # the head of the partition is most efficient
                else: # the head of a partition was more efficient then our current best
                    most_efficient = most_efficient_partition

                    # we know that i is the most efficient which means i+spacing was not valid and i-* are less than i
                    # however we still need to test i+1:i+spacing and compare those answers to i
                    start = most_efficient[len(most_efficient) - 1] + 1
                    spacing = int(ceil(spacing / partitions))


            return most_efficient

    return list(
        map(lambda i: all_items[i],
                _subset_sum(
                    start=0,
                    remaining_money=total_money,
                    remaining_gifts=total_gifts
                )[1:]
        )
    )

if __name__ == "__main__":
    parser = ArgumentParser(
        prog="Challenge #2",
        description="Finds the combination of gifts that finds the combination of gifts that most closely meets the `total_value`"
    )

    parser.add_argument(
        "file_path",
        help="Path to the datafile"
    )

    parser.add_argument(
        "total_value",
        help="The total value of the gift card",
        type=int
    )

    parser.add_argument(
        "--gifts",
        help="The number of gifts being purchased",
        default=2,
        type=int
    )

    parser.add_argument(
        "--max_threads",
        help="The Maximum Number of Threads To Use",
        default=1,
        type=int
    )

    parser.add_argument(
        "--partitions",
        help="Number of subroutines done in parallel",
        default=1,
        type=int
    )

    args = vars(parser.parse_args())

    if args['total_value'] < 0:
        raise Exception('total_value must be positive')

    if args['gifts'] <= 0:
        raise Exception('gifts must be positive')

    if args['partitions'] < 1:
        raise Exception('must have at least 1 partitions to ensure completion')

    items = open(args['file_path'], 'rb').readlines()
    indexes = range(len(items))
    indexed_items = list(zip(indexes, items))

    # Setup parallelism pool
    pool = Pool(int(pow(len(indexed_items), args['gifts'])))
    items_list = pool.map(parse_line, indexed_items)

    results = subset_sum(
        total_money=args['total_value'],
        all_items=items_list,
        total_gifts=args['gifts'],
        partitions=args['partitions'],
        thread_pool=pool
    )
    results.reverse()
    if len(results) == 0:
        print("Not Possible")
    else:
        print(reduce(lambda a,b: a+", "+b, map(lambda item: "%s %d" % (item['item'], item['price']),results)))