from lib import utilities
import git
from os import listdir
from os.path import isfile, join 

# This is the Scipy attribute. This attribute attempts to figure out if a github repo
# is a scipy project. It does this by cloning the repo, and then reading all the 
# files in the repo and checking if the file contents contain the keyword 'Scipy'.

def run(project_id, repo_path, cursor, **options):
    cursor.execute('''
        SELECT
            url
        FROM
            projects
        WHERE
            id = {0}
        '''.format(project_id))

    record = cursor.fetchone()

    # Trim the value right from the database
    full_url = utilities.TOKENIZER.tokenize(record[0].rstrip()) 
    
    # Perform git clone on the repo
    git.Git('./clones').clone(full_url)
    
    lastslash = full_url.rfind('/')

    mypath = './clones' + full_url[lastslash:]

    # Get all the files inside the directory
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    print onlyfiles

    i = 0
    counter = 0
    while i < len(onlyfiles) :
        file = onlyfiles[i]
        fileDescriptor = open(file, "r") 
        content = fileDescriptor.read()

        if content.indexOf("Scipy") ! = -1
            counter++ 

    return counter

if __name__ == '__main__':
    print('Attribute plugins are not meant to be executed directly.')
else:
    from lib.core import Tokenizer
    from lib.utilities import url_to_json

