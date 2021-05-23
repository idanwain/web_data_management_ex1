import sys
import ontology_builder
import query_executer

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        print("Please enter an argument.")
        sys.exit(0)
    if args[1] == 'create':
        ontology_builder.create()
    elif args[1] == 'question':
        if len(args) < 3:
            print("Please enter a question.")
            sys.exit(0)
        question = str(args[2])
        query_executer.execute(question)

