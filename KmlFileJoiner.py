from glob import glob
import re
import jinja2

from KmlFile import KmlFile

templateLoader = jinja2.FileSystemLoader(searchpath=".")
templateEnv = jinja2.Environment(loader=templateLoader)

IGNORED_FILES = ["kml_template.kml", "JoinedFile.kml"]

def user_input_parser(user_input):
    """Parses user input and filters the kml files accordingly."""
    if user_input == "All":
        return [f for f in kml_files if f.file_name not in IGNORED_FILES]
    else:
        file_nums = re.split(r"[,;\s]", user_input.strip())

    try:
        return [kml_files[int(num)] for num in file_nums]
    except ValueError:
        raise RuntimeError("Invalid input, please try again.")
    except IndexError:
        raise RuntimeError("List contains invalid number, please try again.")

def join_files(new_file_name, template_name, kml_files):
    kml_files.sort(key=lambda x: x.first_entry[0])

    data = []
    for kml_file in kml_files:
        for entry in kml_file.entries:
            data.append(entry)

    template = templateEnv.get_template(template_name)
    with open(new_file_name, 'w') as new_file:
        new_file.write(template.render(data=data))

if __name__ == "__main__":
    kml_files = [KmlFile(file_name) for file_name in glob('*.kml')]

    print "Available files to join are:"
    for ii, kml_file in enumerate(kml_files):
        if kml_file.file_name not in IGNORED_FILES:
            print " {}\t{}".format(ii, kml_file.file_name)

    for attempts in range(5):
        try:
            selected_files = user_input_parser(
                raw_input("Enter a list of files to join or type 'All':\n"))
            break
        except RuntimeError as error:
            print error.args[0]
    else:
        print "Failed to understand input. Goodbye."
        exit()

    print ", ".join([f.file_name for f in selected_files])

    join_files("JoinedFile.kml", "kml_template.kml", selected_files)
