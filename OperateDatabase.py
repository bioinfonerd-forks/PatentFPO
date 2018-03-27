import sqlite3

cx = sqlite3.connect('patents_FPO_ver2.db')
cu = cx.cursor()

cu.execute('create table if not exists patents_info '
           '('
           'id integer primary key, '
           'title varchar(30), '
           'app_num varchar(36) UNIQUE, '
           'abstract varchar(1000), '
           'inventor varchar(50),'
           'pub_date varchar(20), '
           'fil_date varchar(20), '
           'assignee varchar(30), '
           'score varchar(5)'
           ')')


# utils = {'Title': 'title',
#          'Inventors': 'inventor',
#          'Application Number': 'app_num',
#          'Abstract': 'abstract',
#          'Publication Date': 'pub_date',
#          'Filing Date': 'fil_date',
#          'Assignee': 'assignee',
#          }

cx.commit()
cu.close()
cx.close()


def insert_data(data_dict):
    cx = sqlite3.connect('patents_FPO_ver2.db')
    cu = cx.cursor()
    _sql = 'INSERT INTO patents_info '
    _d1 = '('
    _d2 = '('
    for k, v in data_dict.items():
        _d1 += str(k) + ', '
        _d2 += '\"' + str(v) + '\"' + ', '
    _d1 = _d1[:-2] + ')'
    _d2 = _d2[:-2] + ')'

    _sql += _d1 + ' VALUES ' + _d2

    # print(_sql)
    cu.execute(_sql)
    cx.commit()
    cu.close()
    cx.close()
