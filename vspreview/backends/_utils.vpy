
#https://stackoverflow.com/questions/11990556/how-to-make-global-imports-from-a-function
def my_imports(module_name,alias_name):
    if(alias_name == ""):
       alias_name=module_name
    globals()[alias_name] = __import__(module_name)
