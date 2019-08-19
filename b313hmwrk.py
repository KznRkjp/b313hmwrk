def value_strip(value):    #убираем лишнее в values
    if type(value) is tuple:
        result = ''
        for i in value:
            result+=str(i)
            result+=' '
        return result.strip(' ')
    else:
        return value


class Tag:
    def __init__(self, tag,  toplevel=False, is_single=False, **kwargs):
        self.tag = tag
        self.text = ""
        self.toplevel = toplevel
        self.is_single = is_single
        self.children = []
        self.attributes = {}
        for attr_name, attr_value in kwargs.items():
            self.attributes[attr_name]=attr_value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


    def __iadd__(self, other):
        self.children.append(other)
        return self


    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value_strip(value)))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "%s" % self.text
            for child in self.children:
                internal +="\n"
                internal += str(child)

            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)

            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )

# ...
class HTML:
    def __init__(self, output, tag='html'):
        self.tag = tag
        self.children = []
        self.output = output

    def __enter__(self):
        return self

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __exit__(self, type, value, traceback):
        result =''
        if self.children:
            opening = "<{tag}>".format(tag=self.tag)
            internal = "\n"
            for child in self.children:
                internal += str(child)
                internal +="\n"
            ending = "</%s>" % self.tag
            result = opening + internal + ending
        else:
            result = "<%s>" % self.tag
            result+= "</%s>" % self.tag
        if self.output is None:
            print (result)
        else:
            with open(self.output,'w') as fp:
                fp.write(result)
        return self






class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.attributes = {}
        self.children = []
        for attr_name, attr_value in kwargs.items():
            self.attributes[attr_name]=attr_value

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __iadd__(self, other):
        self.children.append(other)
        return self


    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)


        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            internal = "\n"
            for child in self.children:
                internal += str(child)
                internal += "\n"
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            return "<{tag} {attrs}></{tag}>".format(
                    tag=self.tag, attrs=attrs
                )



if __name__ == "__main__":
    with HTML(output='hmrk.html') as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title

            doc += head


        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text")) as h1:
                h1.text = "Test"
                body += h1
            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph
                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img
                body += div
            doc += body



# <html>
# <head>
#   <title>hello</title>
# </head>
# <body>
#     <h1 class="main-text">Test</h1>
#     <div class="container container-fluid" id="lead">
#         <p>another test</p>
#         <img src="/icon.png" data-image="responsive"/>
#     </div>
# </body>
# </html>
