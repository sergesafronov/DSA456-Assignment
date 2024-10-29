#
#   Author: Catherine Leung
#   These are the unit tests for functions and classes of assingment 1 part D
#   To use this, run: python test_a1_partd.py

import unittest
from collections import Counter
from a1_partd import get_overflow_list, overflow
from a1_partc import Queue

class A1DTestCase(unittest.TestCase):
    """These are the test cases for functions and classes of a1"""
    
    def test_get_overflow_list(self):

        def gen_id(row,col):
            return row * 100 + col

        grid =[[0, 0, 0, 0, 0, 0 ,0],
               [0, 0, 0, 0, 0, 0 ,0],
               [0, 0, 0, 0, 0, 0 ,0],
               [0, 0, 0, 0, 0, 0 ,0],
               [0, 0, 0, 0, 0, 0 ,0], 
               [0, 0, 0, 0, 0, 0 ,0]
               ]
        result = get_overflow_list(grid)
        self.assertEqual(result, None)


        grid =[[1, 2, 2, 2, 2, 2 , 2, 1],
               [2, 3, 3, 3, 3, 3 , 3, 2],
               [2, 3, 3, 3, 3, 3 , 3, 2],
               [2, 3, 3, 3, 3, 3 , 3, 2],
               [2, 3, 3, 3, 3, 3 , 3, 2],
               [2, 3, 3, 3, 3, 3 , 3, 2],
               [1, 2, 2, 2, 2, 2 , 2, 1]
               ]

        result = get_overflow_list(grid)
        self.assertEqual(result, None)



        grid =[[-1, -2, -2, -2, -2, -2 , -2, -1],
               [-2, -3, -3, -3, -3, -3 , -3, -2],
               [-2, -3, -3, -3, -3, -3 , -3, -2],
               [-2, -3, -3, -3, -3, -3 , -3, -2],
               [-2, -3, -3, -3, -3, -3 , -3, -2],
               [-2, -3, -3, -3, -3, -3 , -3, -2],
               [-1, -2, -2, -2, -2, -2 , -2, -1]
               ]

        result = get_overflow_list(grid)
        self.assertEqual(result, None)


        grid =[[2,  0,  0, 0, 0],
                [0, -3,  0, 0, 0],
                [0,  0, -2, 0, 0],
                [-1, 0,  0, 0, 3]
                ]
        correct = [(0,0),(3,4)]
        overflow_hash = Counter()
        for coord in correct:
            overflow_hash[gen_id(coord[0],coord[1])] += 1

        result = get_overflow_list(grid)

        self.assertEqual(len(correct), len(result))

        for coord in result:
            self.assertEqual(overflow_hash[gen_id(coord[0],coord[1])], 1)
            overflow_hash[gen_id(coord[0],coord[1])] += 1

        grid =[[-2,  0,  0, 0, 0],
                [0, 3,  0, 0, 0],
                [0,  0, 2, 0, 0],
                [1, 0,  0, 0, -3]
                ]

        correct = [(0,0),(3,4)]
        overflow_hash = Counter()
        for coord in correct:
            overflow_hash[gen_id(coord[0],coord[1])] += 1

        result = get_overflow_list(grid)

        self.assertEqual(len(correct), len(result))

        for coord in result:
            self.assertEqual(overflow_hash[gen_id(coord[0],coord[1])], 1)
            overflow_hash[gen_id(coord[0],coord[1])] += 1



        grid =[
                [2, 3, 3, 3, 3, 2],
                [3, 4, 4, 4, 4, 3],
                [3, 4, 4, 4, 4, 3],
                [3, 4, 4, 4, 4, 3],
                [2, 3, 3, 3, 3, 2]

            ]

                                                        
        correct = [(0,0), (0,1), (0,2), (0,3),(0,4),(0,5),
                   (1,0), (1,1), (1,2), (1,3),(1,4),(1,5),
                   (2,0), (2,1), (2,2), (2,3),(2,4),(2,5),
                   (3,0), (3,1), (3,2), (3,3),(3,4),(3,5),
                   (4,0), (4,1), (4,2), (4,3),(4,4),(4,5)
                 ]
        overflow_hash = Counter()
        for coord in correct:
            overflow_hash[gen_id(coord[0],coord[1])] += 1

        result = get_overflow_list(grid)
        self.assertEqual(len(correct), len(result))

        for coord in result:
            self.assertEqual(overflow_hash[gen_id(coord[0],coord[1])], 1)
            overflow_hash[gen_id(coord[0],coord[1])] += 1



    def test_overflow(self):
        original = [
            [ 
                [-2,  2, -3,  0,  0],
                [ 0, -4,  0,  0,  0],
                [ 0,  0,  3,  0,  1],
                [-1,  0,  0,  0,  1]
            ],
            [
                [-1,  3,   3,  0,  0],
                [ 0, -3,   0,  0,  0],
                [ 0,  0,  -3,  0,  2],
                [-1,  0,  -2, -2,  2]
            ],

            [
                [ 1,  2,   2,  0,  0],
                [ 0, -3,   0,  0,  0],
                [ 0,  0,  -3,  0,  2],
                [-1,  0,  -2, -2,  1]
            ],
            [
                [ 1,  3,   3,  0,  0],
                [ 0,  3,   0,  0,  0],
                [ 0,  0,   3,  0,  2],
                [ 1,  0,   2,  2,  2]
            ],
            [
                [ -1, -3,   -3,  0,   0],
                [  0, -3,    0,  0,   0],
                [  0,  0,   -3,  0,  -2],
                [ -1,  0,   -2, -2,  -2]
            ],
        ]
        steps = [
                    [
                     [  0,  -5,  0,  -1,  0 ],
                     [ -2,   0, -2,   0,  0 ],
                     [  0,  -1,  3,   0,  1 ],
                     [ -1,   0,  0,   0,  1 ]
                    ],
                    [
                     [ -1,   0,  -1,  -1,  0 ],
                     [ -2,  -1, -2,   0,  0 ],
                     [  0,  -1,  3,   0,  1 ],
                     [ -1,   0,  0,   0,  1 ]
                    ],
                    [
                     [  2,   1,  1,  1,  0 ],
                     [  0,   4,  1,  0,  0 ],
                     [  0,   0, -3,  0,  3 ],
                     [ -1,   0, -2,  3,  0 ]
                    ],
                    [
                     [  0,   3,  1,  1,  0 ],
                     [  2,   0,  2,  0,  1 ],
                     [  0,   1, -3,  2,  0 ],
                     [ -1,   0,  3,  0,  2 ]
                    ],
                    [
                     [  1,   0,  2,  1,  0 ],
                     [  2,   1,  2,  0,  1 ],
                     [  0,   1,  4,  2,  1 ],
                     [ -1,   1,  0,  2,  0 ]
                    ],

                    [
                     [  1,   0,  2,  1,  0 ],
                     [  2,   1,  3,  0,  1 ],
                     [  0,   2,  0,  3,  1 ],
                     [ -1,   1,  1,  2,  0 ]
                    ]


                ]



        the_queue = Queue()
        grid = []
        for i in range(len(original[0])):
            grid.append(original[0][i].copy())

        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 2)
        self.assertEqual(len(the_queue), 2)
        for i in range(len(the_queue)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i])
        self.assertEqual(grid,tmp)



        grid = []
        for i in range(len(original[1])):
            grid.append(original[1][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 4)
        self.assertEqual(len(the_queue), 4)
        for i in range(len(the_queue)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i + 2])
        self.assertEqual(grid,tmp)

        grid = []
        for i in range(len(original[2])):
            grid.append(original[2][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 0)
        self.assertEqual(grid,original[2])


        grid = []
        for i in range(len(original[3])):
            grid.append(original[3][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 0)
        self.assertEqual(grid,original[3])


        grid = []
        for i in range(len(original[4])):
            grid.append(original[4][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 0)
        self.assertEqual(grid,original[4])

        grid = []
        for i in range(len(original[0])):
            grid.append(original[0][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 2)
        self.assertEqual(len(the_queue), 2)

        grid = []
        for i in range(len(original[1])):
            grid.append(original[1][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 4)
        self.assertEqual(len(the_queue), 6)

        grid = []
        for i in range(len(original[2])):
            grid.append(original[2][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 6)

        grid = []
        for i in range(len(original[3])):
            grid.append(original[3][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 6)


        grid = []
        for i in range(len(original[4])):
            grid.append(original[4][i].copy())
        rc = overflow(grid,the_queue)
        self.assertEqual(rc, 0)
        self.assertEqual(len(the_queue), 6)


        for i in range(len(steps)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i])



    def test_overflow2(self):


        grid =[ 
                [ 2 , -2,   -1, 0, 0,  0],
                [ 2,  0 , 0,  0,  0,  0],
                [ 1,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, -1]
              ]


        steps = [
                    [
                    [ 0 , 3,  -1, 0, 0,  0],
                    [ 3,  0 , 0,  0,  0,  0],
                    [ 1,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, -1]
                     ],
                    [
                    [ 2 , 0,  2,  0, 0,  0],
                    [ 0,  2 , 0,  0,  0,  0],
                    [ 2,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, -1]
                    ],
                    [
                    [ 0 , 1,  2,  0, 0,  0],
                    [ 1,  2 , 0,  0,  0,  0],
                    [ 2,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, -1]
                    ]
                ]
        




        the_queue = Queue()

        rc = overflow(grid,the_queue)


        self.assertEqual(rc, 3)

        for i in range(len(steps)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i])

        self.assertEqual(tmp,grid)
 

    def test_overflow3(self):


        grid =[ 
                [ 2 , -2,   -2, 0, 0,  0],
                [ 2,  0 , 3,  0,  0,  0],
                [ 1,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, 0]
              ]


        steps = [
                    [
                    [ 0 , 3,  -2, 0, 0,  0],
                    [ 3,  0 , 3,  0,  0,  0],
                    [ 1,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]
                     ],
                    [
                    [ 2 , 0,  3,  0, 0,  0],
                    [ 0,  2 , 3,  0,  0,  0],
                    [ 2,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0]
                    ],
                ]

        the_queue = Queue()

        rc = overflow(grid,the_queue)


        self.assertEqual(rc, 2)

        for i in range(len(steps)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i])

        self.assertEqual(tmp,grid)


    def test_overflow4(self):

        grid =[ 
                [ 2 , -2,   -1, 0, 0,  0],
                [ 2,  0 , 0,  0,  0,  0],
                [ 1,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, 0],
                [ 0,  0,  0,  0,  0, 1]
              ]


        steps = [
                    [
                    [ 0 , 3,  -1, 0, 0,  0],
                    [ 3,  0 , 0,  0,  0,  0],
                    [ 1,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 1]
                     ],
                    [
                    [ 2 , 0,  2,  0, 0,  0],
                    [ 0,  2 , 0,  0,  0,  0],
                    [ 2,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 0],
                    [ 0,  0,  0,  0,  0, 1]
                    ]
                ]
        




        the_queue = Queue()

        rc = overflow(grid,the_queue)


        self.assertEqual(rc, 2)

        for i in range(len(steps)):
            tmp = the_queue.dequeue()
            self.assertEqual(tmp,steps[i])

        self.assertEqual(tmp,grid)




if __name__ == '__main__':
    unittest.main()
