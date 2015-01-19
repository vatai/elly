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
    if not os.path.exists(id):
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


def modify_file():
    fn1 = generate_random_file()
    fn2 = fn1 + '.bak'
    shutil.copyfile(fn1,fn2)


def randfilename(n=10):
    return ''.join([ random.choice(string.ascii_letters) for _ in range(n) ])


def gen_file_test(session):
    # make two files
    rv = None
    name = session['filename'].split('.pas')[0]
    
    for _ in range(10):
        n = str(random.randrange(100))
        
        sol_outfile = randfilename()
        sol_input = '\n'.join([sol_outfile,n])
        sol_cmd = ['./' + session['problem_id']]

        exe_outfile = randfilename()
        exe_cmd = [name]
        exe_input = '\n'.join([exe_outfile,n])

        # run the solution
        sol_output = check_output( sol_cmd, input=sol_input,
                                   universal_newlines=True, stderr=STDOUT)

        # run the candidate solution
        try:
            exe_output = check_output( exe_cmd, input=exe_input,
                                   universal_newlines=True, stderr=STDOUT)
        except CalledProcessError as e:
            rv = 'A program nem futot le sikeresen!\n{}'.format(e.output)

        # check the result
        if not filecmp.cmp(sol_outfile,exe_outfile,shallow=False):
            rv = 'Fájlok különböznek...'

        os.remove(sol_outfile)
        os.remove(exe_outfile)

    return rv
