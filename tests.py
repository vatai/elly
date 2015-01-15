from subprocess import check_output,STDOUT,CalledProcessError 

import os,glob,re,string,random,filecmp,tempfile,shutil

COMPILER = "fpc"


def compile_pas(filename):
    print('Compiling {}'.format(filename))
    cmd = [COMPILER,filename]
    try:
        out = check_output(cmd,stderr=STDOUT)
        return (0,out.decode('UTF-8'))
    except CalledProcessError as e:
        return (e.returncode,e.output.decode('UTF-8'))


def compilesolution(id):
    fn = id+'.pas'
    if not os.path.exists(fn) or not os.access(fn, os.X_OK):
        compile_pas(fn)


def generate_random_file( n=80, nl=10, contents=string.printable):
    FNLENGTH = 8

    (f,filename) = tempfile.mkstemp(text=True)
    f = os.fdopen(f,'w')
    for j in range(nl):
        for i in range(n):
            f.write(random.choice(contents))
        if nl!=0: f.write('\n')
    f.close()

    return filename


    
def runtest():
    # make two files
    fn1 = generate_random_file()
    fn2 = fn1 + '.bak'
    shutil.copyfile(fn1,fn2)
    inputs='\na\nb\n'

    # run the solution
    solution_cmd = ['./' + session['problem_id']]
    print(fn1+inputs)
    solution_output = check_output( solution_cmd,
                                    input=fn1+inputs,
                                    universal_newlines=True,
                                    stderr=STDOUT)

    # run the candidate solution
    exe_cmd = [session['filename'].split('.pas')[0]]
    rv = None
    try:
        print(fn2+inputs)
        output = check_output( exe_cmd, input=fn2+inputs,
                               universal_newlines=True, stderr=STDOUT)
    except CalledProcessError as e:
        rv = 'A program nem futot le!\n{}'.format(e.output)


    # check the result
    if not filecmp.cmp(fn1,fn2,shallow=True):
        rv = 'Fájlok különböznek...'
    os.remove(fn1)
    os.remove(fn2)
    return rv
