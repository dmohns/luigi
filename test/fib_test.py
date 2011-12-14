import datetime, os
from spotify import luigi
from spotify.util.test import *
from spotify.luigi.mock import MockFile

File = luigi.File

# Calculates Fibonacci numbers :)

@luigi.expose
class Fib(luigi.Task):
    n = luigi.IntParameter(default = 100)

    def requires(self):
        if self.n >= 2: return [Fib(self.n - 1), Fib(self.n - 2)]
        else: return []

    def output(self):
        return File('/tmp/fib_%d' % self.n)

    def run(self):
        if self.n == 0:
            s = 0
        elif self.n == 1:
            s = 1
        else:
            s = 0
            for input in self.input():
                for line in input.open('r'):
                    s += int(line.strip())

        f = self.output().open('w')
        f.write('%d\n' % s)
        f.close()

class FibTest(TestCase):
    def setUp(self):
        global File
        File = MockFile
        MockFile._file_contents.clear()
        
    def test_invoke(self):
        s = luigi.scheduler.LocalScheduler()
        s.add(Fib(100))
        s.run()

        self.assertEqual(MockFile._file_contents['/tmp/fib_10'], '55\n')
        self.assertEqual(MockFile._file_contents['/tmp/fib_100'], '354224848179261915075\n')

    def test_cmdline(self):
        luigi.run(['--local-scheduler', 'Fib', '--n', '100'])

        self.assertEqual(MockFile._file_contents['/tmp/fib_10'], '55\n')
        self.assertEqual(MockFile._file_contents['/tmp/fib_100'], '354224848179261915075\n')

if __name__ == '__main__':
    luigi.run()
