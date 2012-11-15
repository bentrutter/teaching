import os, rwkos, spreadsheet

import txt_mixin

import group_rst_parser
reload(group_rst_parser)

from IPython.core.debugger import Pdb

class_folder = rwkos.FindFullPath('siue/classes/482/2012/')
group_path = os.path.join(class_folder, 'group_list.csv')
group_list = spreadsheet.group_list_2010(group_path)
#group_path = os.path.join(class_folder, 'planning/mini_project/team_list.csv')
#group_list = spreadsheet.mini_project_group_list(group_path)

alts = {'Bahrns':'Chris', \
        'Barnes':'Alex', \
        'Casey':'Jeff', \
        'Knauer':'Chris', \
        'Phillips':'Joe', \
        'Rickert':'Chris', \
        'Fehrenbacher':'Joe', \
        'Coleman':'Matt', \
        'Tripp':'Matt', \
        'Sprehe':'Dan', \
        'Strackeljahn':'Dan', \
        }

inverse_alts = {'Chris':'Christopher', \
                'Joe':'Joseph', \
                'Alex':'Alexander', \
                }


email_path = rwkos.FindFullPath('siue/classes/482/2012/email_list_ME482_Fall_2012.csv')
email_list = spreadsheet.email_list(email_path)

#from IPython.core.debugger import Pdb


def file_name_from_group_name(group_name, ext='.rst'):
    filename = group_name.replace(' ','_') + ext
    return filename


def path_from_name(name):
    pathout = name.replace(' ','_') + '.rst'
    return pathout


class group(object):
    def __init__(self, group_name):
        self.group_name = group_name
        self.find_members()


    def fix_dup_firsts(self):
        for name in self.firstnames:
            inds = self.firstnames.findall(name)
            if len(inds) > 1:
                print('found dup.:' + name)
                for ind in inds:
                    initial = ' ' + self.lastnames[ind][0] + '.'
                    self.firstnames[ind] += initial


    def strip_names(self):
        firstnames = [item.strip() for item in self.firstnames]
        self.lastnames = [item.strip() for item in self.lastnames]
        self.firstnames = txt_mixin.txt_list(firstnames)


    def find_members(self):
        lastnames, firstnames = group_list.get_names(self.group_name)
        self.lastnames = lastnames
        self.firstnames = firstnames
        self.firstnames = txt_mixin.txt_list(firstnames)
        for n, lastname in enumerate(lastnames):
            if alts.has_key(lastname):
                self.firstnames[n] = alts[lastname]
        self.strip_names()
        self.fix_dup_firsts()
        self.names = zip(self.firstnames, self.lastnames)


    def build_name_str(self):
        N = len(self.names)
        if N == 1:
            self.name_str = ' '.join(self.names[0])
        else:
            name_str = ''
            for n, pair in enumerate(self.names):
                if n > 0:
                    name_str +=', '
                if n == (N-1):
                    name_str += 'and '
                name_str += pair[0] + ' ' + pair[1]
            self.name_str = name_str


class_dict = {'Literature Review':group_rst_parser.lit_review, \
              'Contemporary Issues':group_rst_parser.contemp_issues, \
              'Writing: Quick Read':group_rst_parser.quick_read, \
              'Writing: Slow Read':group_rst_parser.slow_read, \
              'Content':group_rst_parser.content_sec, \
              'Extra Credit':group_rst_parser.extra_credit}


class group_with_rst(group_rst_parser.group_with_rst):
    def __init__(self, pathin, subre='^-+$', alts=alts, \
                 subclass=group_rst_parser.section_level_1, \
                 class_dict=None):
        group_rst_parser.group_with_rst.__init__(self, \
                                                 pathin, \
                                                 subre=subre,
                                                 subclass=subclass)
        self.group_list = group_list
        self.email_list = email_list
        self.find_members()
        if self.class_dict is None:
            self.class_dict = class_dict
        self.break_into_sections()

class problem_statement(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.1

class design(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.25

class analysis(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.25

class computers_and_software(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.05

class timeline(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.05

class budget(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.05

class quick_read(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.05

class slow_read(group_rst_parser.lit_review):
    def __init__(self, *args, **kwargs):
        group_rst_parser.lit_review.__init__(self, *args, **kwargs)
        self.weight = 0.20


design_paper_dict = {'Problem Statement':problem_statement, \
                     'Design':design, \
                     'Analysis':analysis, \
                     'Computers and Software':computers_and_software, \
                     'Timeline':timeline, \
                     'Budget':budget, \
                     'Writing: Quick Read':quick_read, \
                     'Writing: Slow Read':slow_read}


class design_paper_rst(group_with_rst):
    def __init__(self, *args, **kwargs):
        kwargs['class_dict'] = design_paper_dict
        group_with_rst.__init__(self, *args, **kwargs)


    def calc_overall_score(self, debug=0):
        grades = None
        total = 0.0
        w_total = 0.0
        for section in self.sec_list:
            if hasattr(section,'grade'):
                elem = float(section.grade)
                weight = float(section.weight)
                total += elem*10.0*weight#all scores are out of 10
                if elem > 0:
                    w_total += weight
                if grades is None:
                    grades = [elem]
                else:
                    grades.append(elem)
                if debug:
                    print('elem = '+str(elem))
                    print('weight = '+str(weight))
                    print('total = '+str(total))
        #Pdb().set_trace()
        self.ave = total
        self.ave_so_far = total/w_total
        self.overall_grade = self.ave_so_far
        return self.ave

    def build_spreadsheet_row(self):
        group_with_rst.build_spreadsheet_row(self)
        #self.row_out.append(self.ave_so_far)
        return self.row_out

    def get_section_labels(self):
        group_with_rst.get_section_labels(self)
        #self.labels.append('Ave. So Far')
        return self.labels
