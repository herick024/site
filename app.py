import web
import data_file
from web import form



data = data_file.Data_file()
data.data_read('data/data.json')
tienda = data.data_campo('Nom_Ent')

db = web.database(dbn='mysql', db='gaming', user='root', pw='momantay')

urls = (
    '/','index',
    '/analisis', 'analisis',
    '/crud', 'crud',
    '/login','login'
)

render = web.template.render('templates/', base = 'base')
vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
vemail = form.regexp(r".*@.*", "must be a valid email address")

register_form = form.Form(
    form.Textbox("username", description="Username"),
    form.Password("password", vpass, description="Password"),
    form.Password("password2", description="Repeat password"),
    form.Button("submit", type="submit", description="Register"),
    validators = [
        form.Validator("Passwords did't match", lambda i: i.password == i.password2)])

login = form.Form(
    form.Textbox('username'),
    form.Password('password'),
    form.Button('Login'),
)

data_form = form.Form(
    form.Dropdown('Estado',data.data_campo('Nom_Ent')),
    form.Dropdown('Grupo', data.data_campo('GpoEdad')),
      
)

formG = form.Form(
    form.Textbox("Nombre"),
    form.Textbox("Puntuacion",size="1",maxlength="2"),
    form.Textbox('Genero'),
    form.Textbox('Descripcion'))



class index:        
    def GET(self):
        return render.index()

class analisis:
    def GET(self):
        formD = data_form
        return render.analisis(formD,None,None,None)

    def POST(self):
        formD = data_form
        if not formD.validates():
            return render.analisis(formD,None,None,None)
        else:  
            print formD['Estado'].value,formD['Grupo'].value
            
            return render.analisis(formD, data.data_get(),formD['Estado'].value,formD['Grupo'].value)

class crud:
    def GET(self):
        formN = formG
        result = db.select('games')
        return render.crud(formN, result) 

    def POST(self):
        formN = formG
        if not formN.validates():
            result = db.select('games')
            return render.crud(form,result)
        else:
            db.insert('games',nombre=formN.d.Nombre,puntuacion=formN.d.Puntuacion,genero=formN.d.Genero,descripcion=formN.d.Descripcion)
            result = db.select('games')
            return render.crud(form,result)

class login:
    def GET(self):
        f = login()
        return render.login(f)

class register:
    def GET(self):
        form = register_form
        return render.register(form)    
       
if __name__ == "__main__":
    app = web.application(urls, globals())
    web.internalerror = web.debugerror
    app.run()