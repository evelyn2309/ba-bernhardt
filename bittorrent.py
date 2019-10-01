class Bittorrent(object):
    def __init__(self):
        pass

    @staticmethod
    def chunk_it(seq, n):
        """
        Function to chunk a sequence.
        :param seq: must be string or bytes.
        :param n: must be integer.
        :return: list of chunks.
        """

        avg = len(seq) / float(n)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out
