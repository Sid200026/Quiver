from django import template

register = template.Library()


@register.filter(is_safe=True, name="errorOnly")
def getErrorOnly(value):
    temp = str(value)
    start_string = "<li>"
    end_string = "</li"
    start_index = temp.find(start_string) + 4
    end_index = temp.find(end_string)
    return temp[start_index:end_index]
