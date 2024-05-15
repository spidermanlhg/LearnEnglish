import sys,os
def test(xx):
    print( "hello:"+ xx  )


a,b=5,4

if __name__ == "__main__":
    test( sys.argv[1] )
    print(dir())

