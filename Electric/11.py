from traits.api import HasTraits,Range,Enum,List,HasStrictTraits
from traitsui.api import View,Item,TableEditor,Group
from traitsui.table_column import ObjectColumn

class Person(HasTraits):
    name = str
    age = Range(low=0,value=20)

def f1():
    p = Person(name = "111")
    p.configure_traits()

f1()

personTables = TableEditor(columns=[
    ObjectColumn(name = 'name',width = 0.2),
    ObjectColumn(name='age',width=0.2)],
    edit_view = View(Group('name','age')),
    row_factory=Person)

class Department(HasStrictTraits):
    persons = List(Person)
    traits_view = View(
    Group(
        Item('persons',
                show_label=False,
                editor=personTables
                ),
        show_border=True,
    ),
    title='TableEditor',
    width=.4,
    height=.4,
    resizable=True,
    buttons=['OK'],
    kind='live'
    )
ps = [Person(name = '11',age=1)]
dp = Department(persons = ps)
dp.configure_traits()
