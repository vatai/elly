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
        try:
            sol_output = check_output( sol_cmd, input=sol_input,
                                       universal_newlines=True, stderr=STDOUT)
        except CalledProcessError as e:
            rv = 'Valami baj van, szólj a tanárnak!\n{}'.format(e.output)

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

def chk_ast_output(session):
    print('chk_ast_output')
    # make two files
    rv = None
    name = session['filename'].split('.pas')[0]
    
    sol_cmd = ['./' + session['problem_id']]
    exe_cmd = [name]

    for ii in range(10):
        print('loop {}'.format(ii))
        n = random.randrange(20)+1
        
        sol_input = [random.choice(string.ascii_letters) for _ in range(n)]
        sol_input = '\n'.join(sol_input) + '\n*\n'

        exe_input = sol_input

        print('Execution started')
        print(bytes(sol_input,'utf8'))
        # run the solution
        try:
            sol_output = check_output( sol_cmd, input=sol_input,
                                       universal_newlines=True, stderr=STDOUT)
        except CalledProcessError as e:
            rv = 'Valami baj van, szólj a tanárnak!\n{}'.format(e.output)
        print('Solution executed.')

        # run the candidate solution
        try:
            exe_output = check_output( exe_cmd, input=exe_input,
                                   universal_newlines=True, stderr=STDOUT)
        except CalledProcessError as e:
            rv = 'A program nem futot le sikeresen!\n{}'.format(e.output)
        print('Candidate executed.')

        # check the result
        if sol_output != exe_output:
            rv = 'Nem azt írja ki a program amit kellene!\n'
            rv = rv + 'A megoldás kimenete:\n{}'.format(sol_output)
            rv = rv + 'A te programod kimenete:\n{}'.format(exe_output)


    return rv
