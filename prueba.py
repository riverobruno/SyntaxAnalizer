import ply.lex as lex
import ply.yacc as yacc
import re
import os
import codecs
import tkinter
from tkinter import filedialog
from tkinter import ttk

# Lista de tokens
tokens = ["Article","FinArticle","Itemizedlist","FinItemizedlist","ListItem","FinListItem",
          "Important","FinImportant","Para","FinPara","SimPara","FinSimPara","Emphasis",
          "FinEmphasis","Comment","FinComment","Section","FinSection","Sect1","FinSect1",
          "Info","FinInfo","Title","FinTitle","MediaObject","FinMediaObject","VideoObject",
          "FinVideoObject","VideoData","ImageObject","FinImageObject","ImageData","Abstract",
          "FinAbstract","Address","FinAddress","Street","FinStreet","City","FinCity","State",
          "FinState","Phone","FinPhone","Postcode","FinPostcode","Email","FinEmail","Author",
          "FinAuthor","Name","FinName","Surname","FinSurname","Date","FinDate","Copyright",
          "FinCopyright","Year","FinYear","Holder","FinHolder","Texto","Link","URL"
]


#expresiones regulares y traducciones
def t_Article(t):
    r'<article>'
    return t
def t_FinArticle(t):
    r'</article>'
    return t
def t_Itemizedlist(t):
    r'<itemizedlist>'
    return t
def t_FinItemizedlist(t):
    r'</itemizedlist>'
    return t
def t_ListItem(t):
    r'<listitem>'
    return t
def t_FinListItem(t):
    r'</listitem>'
    return t
def t_Important(t):
    r'<important>'
    return t
def t_FinImportant(t):
    r'</important>'
    return t
def t_Para(t):
    r'<para>'
    return t
def t_FinPara(t):
    r'</para>'
    return t
def t_SimPara(t):
    r'<simpara>'
    return t
def t_FinSimPara(t):
    r'</simpara>'
    return t
def t_Emphasis(t):
    r'<emphasis>'
    return t
def t_FinEmphasis(t):
    r'</emphasis>'
    return t
def t_Comment(t):
    r'<comment>'
    return t
def t_FinComment(t):
    r'</comment>'
    return t
def t_Section(t):
    r'<section>'
    return t
def t_FinSection(t):
    r'</section>'
    return t
def t_Sect1(t):
    r'<sect1>'
    return t
def t_FinSect1(t):
    r'</sect1>'
    return t
def t_Info(t):
    r'<info>'
    return t
def t_FinInfo(t):
    r'</info>'
    return t
def t_Title(t):
    r'<title>'
    #file.write("<title>")
    return t
def t_FinTitle(t):
    r'</title>'
    #file.write("</title>")
    return t
def t_MediaObject(t):
    r'<mediaobject>'
    return t
def t_FinMediaObject(t):
    r'</mediaobject>'
    return t
def t_VideoObject(t):
    r'<videobject>'
    return t
def t_FinVideoObject(t):
    r'</videobject>'
    return t
def t_VideoData(t):
    r'<videodata\s*fileref="(http://|https://|ftp://|ftps://)(\w+\.*\/*\#*\=*\?*\:*\-*)+"/>'
    return t
def t_ImageObject(t):
    r'<imageobject>'
    return t
def t_FinImageObject(t):
    r'</imageobject>'
    return t
def t_ImageData(t):
    r'<imagedata \s* fileref="(http://|https://|ftp://|ftps://)(\w+\.*\/*\#*\=*\?*\:*\-*\_*)+"/>'
    return t
def t_Abstract(t):
    r'<abstract>'
    return t
def t_FinAbstract(t):
    r'</abstract>'
    return t
def t_Address(t):
    r'<address>'
    return t
def t_FinAddress(t):
    r'</address>'
    return t
def t_Street(t):
    r'<street>'
    return t
def t_FinStreet(t):
    r'</street>'
    return t
def t_City(t):
    r'<city>'
    return t
def t_FinCity(t):
    r'</city>'
    return t
def t_State(t):
    r'<state>'
    return t
def t_FinState(t):
    r'</state>'
    return t
def t_Phone(t):
    r'<phone>'
    return t
def t_FinPhone(t):
    r'</phone>'
    return t
def t_Postcode(t):
    r'<postcode>'
    return t
def t_FinPostcode(t):
    r'</postcode>'
    return t
def t_Email(t):
    r'<email>'
    return t
def t_FinEmail(t):
    r'</email>'
    return t
def t_Author(t):
    r'<author>'
    return t
def t_FinAuthor(t):
    r'</author>'
    return t
def t_Name(t):
    r'<firstname>'
    return t
def t_FinName(t):
    r'</firstname>'
    return t
def t_Surname(t):
    r'<surname>'
    return t
def t_FinSurname(t):
    r'</surname>'
    return t
def t_Date(t):
    r'<date>'
    return t
def t_FinDate(t):
    r'</date>'
    return t
def t_Copyright(t):
    r'<copyright>'
    return t
def t_FinCopyright(t):
    r'</copyright>'
    return t
def t_Year(t):
    r'<year>'
    return t
def t_FinYear(t):
    r'</year>'
    return t
def t_Holder(t):
    r'<holder>'
    return t
def t_FinHolder(t):
    r'</holder>'
    return t
def t_URL(t):
    r'(http://|https://|ftp://|ftps://)(\w+\.*\/*\#*\=*\?*\:*\-*)+'
    return t
def t_Link(t):
    r'<link\s*xlink:href="(http://|https://|ftp://|ftps://)(\w+\.*\/*\#*\=*\?*\:*\-*)+"/>'
    return t
def t_Texto(t):
    r'[^<>].[^<>]*'
    return t

def t_N(t):
    r'[0-9]'
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

#gramatica/parser#
def p_ARTICLE(p):
    '''ARTICLE:  TITLE INFO MAS_ARTICLE SECTSS 
    |INFO TITLE MAS_ARTICLE SECTSS
    |INFO MAS_ARTICLE SECTSS
    |TITLE MAS_ARTICLE SECTSS
    |MAS_ARTICLE SECTSS
    |TITLE   INFO   MAS_ARTICLE 
    |INFO   TITLE   MAS_ARTICLE 
    |INFO MAS_ARTICLE 
    |TITLE MAS_ARTICLE 
    |MAS_ARTICLE '''
def p_ABSTRACT(p):
    '''ABSTRACT : Abstract IN_ABSTRACT FinAbstract'''
    
def p_IN_ABSTRACT(p):
    '''IN_ABSTRACT : TITLE SIMPARA PARA
    | TITLE PARA SIMPARA
    | TITLE PARA
    | TITLE SIMPARA
    | SIMPARA PARA
    | PARA SIMPARA
    | PARA
    | SIMPARA'''
    
def p_PARA(p):
    '''PARA : Para IN_PARA FinPara PARA
    | Para IN_PARA FinPara SIMPARA
    | Para IN_PARA FinPara'''
    
def p_IN_PARA(p):
    '''IN_PARA : IN_PARA IN_PARA
    | M
    | ITEMIZEDLIST
    | IMPORTANT
    | ADRESS
    | MEDIAOBJECT'''
    
def p_SIMPARA(p):
    '''SIMPARA : SimPara M FinSimPara SIMPARA
    | SimPara M FinSimPara PARA
    | SimPara M FinSimPara'''
    
def p_ITEMIZEDLIST(p):
    '''ITEMIZEDLIST : Itemizedlist LISTITEM FinItemizedlist'''
    
def p_LISTITEM(p):
    '''LISTITEM : LISTITEM LISTITEM
    | ListItem OTRO FinListItem'''
    
def p_OTRO(p):
    '''OTRO : OTRO OTRO
    | ITEMIZEDLIST
    | PARA
    | SIMPARA
    | ADDRESS
    | MEDIAOBJECT
    | ADRESS
    | COMMENT
    | IMPORTANT
    | ABSTRACT'''
    
def p_IMPORTANT(p):
    '''IMPORTANT : Important TITLE OTRO FinImportant
    | Important OTRO FinImportant'''
    
def p_ADRESS(p):
    '''ADRESS : Address IN_ADRESS FinAddress'''
    
def p_IN_ADRESS(p):
    '''IN_ADRESS : IN_ADRESS  IN_ADRESS
    | Texto
    | STREET 
    | CITY
    | STATE
    | PHONE
    | EMAIL'''
    
def p_STREET(p):
    '''STREET : Street D  FinStreet'''
    
def p_CITY(p):
    '''CITY : City D FinCity'''
    
def p_STATE(p):
    '''STATE : State D FinState'''
    
def p_PHONE(p):
    '''PHONE : Phone NNNNNNNNNN FinPhone'''
    
#def p_INFORMALTABLE(p):
    '''INFORMALTABLE : Informaltable IN_INFTABLE IN_INFTABLE FinInformaltable'''
    
#def p_IN_INFTABLE(p):
    '''IN_INFTABLE : IN_INFTABLE IN_INFTABLE
    | TGROUP
    | MEDIAOBJECT'''

def p_MEDIAOBJECT(p):
    '''MEDIAOBJECT : MediaObject IN_MEDIAOBJECT FinMediaObject'''
    
def p_IN_MEDIAOBJECT(p):
    '''IN_MEDIAOBJECT : INFO VID_IM
    | VID_IM'''
    
def p_VID_IM(p):
    '''VID_IM : VideoObject VIDEOOBJECT FinVideoObject VID_IM
    | VideoObject VIDEOOBJECT FinCideoObject
    | ImageObject IMAGEOBJECT FinImageObject VID_IM
    | ImageObject IMAGEOBJECT FinImageObject'''
    
def p_VIDEOOBJECT(p):
    '''VIDEOOBJECT : INFO VideoData
    | VideoData'''
    
def p_IMAGEOBJECT(p):
    '''IMAGEOBJECT : INFO ImageData
    | ImageData'''
    
def p_INFO(p):
    '''INFO : Info IN_INFO FinInfo'''
    
def p_IN_INFO(p):
    '''IN_INFO : IN_INFO IN_INFO
    | TITLE 
    | MEDIAOBJECT 
    | ABSTRACT 
    | ADDRESS 
    | AUTHOR 
    | DATE 
    | COPYRIGHT'''

def p_TITLE(p):
    '''TITLE : Title IN_TITLE FinTitle'''
    
def p_IN_TITLE(p):
    '''IN_TITLE : IN_TITLE IN_TITLE
    | Texto
    | Link
    | EMAIL
    | EMPHASIS'''
    
def p_EMAIL(p):
   '''EMAIL : Email D FinEmail'''
   
def p_D(p):
    '''D : D D
    | Texto
    | Link
    | EMPHASIS
    | COMMENT'''
    
def p_COMMENT(p):
    '''COMMENT : Comment M FinComment'''
   
def p_EMPHASIS(p):
    '''EMPHASIS : Emphasis M FinEmphasis'''

def p_M(p):
    '''M : M M
    | Texto
    | Link
    | EMAIL
    | EMPHASIS
    | COMMENT
    | AUTHOR'''
    
def p_AUTHOR(p):
    '''AUTHOR : Author FIRSTNAME SURNAME FinAuthor'''
    
def p_FIRSTNAME(p):
    '''FIRSTNAME : Name D FinName FIRSTNAME
    | Name D FinName'''
    
def p_SURNAME(p):
    '''SURNAME : Surname D FinSurname SURNAME
    | Surname D FinSurname'''
    
def p_COPYRIGHT(p):
    '''COPYRIGHT : Copyright IN_COPYRIGHT FinCopyright'''
    
def p_IN_COPYRIGHT(p):
    '''IN_COPYRIGHT : YEAR
    | YEAR HOLDER
    | HOLDER YEAR'''
    
def p_YEAR(p):
    '''YEAR : Year D FinYear YEAR 
    | Year D FinYear'''
    
def p_HOLDER(p):
    '''HOLDER : Holder D FinHolder HOLDER
    | Holder D FinHolder'''
    














parser = yacc.yacc()



#interfaz grafica

def BotonA():
    archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    if archivo:
        Arch = open(archivo, "r")
        a = Arch.read()

        lexer.input(a)
        etiqueta2.configure(state='normal')
        # etiqueta2.delete("1.0", tkinter.END)  # Comentado para conservar el texto previo
        while True:
            tok = lexer.token()
            if not tok:
                break
            etiqueta2.insert(
                tkinter.END, f"Encontré un: {tok.type} Lexema: {tok.value}\n")
        etiqueta2.configure(state='disabled')


def TextoIngresado(event=None):  # Agregado el parámetro 'event'
    text = CajaDeTexto.get()

    lexer.input(text)
    etiqueta2.configure(state='normal')
    # etiqueta2.delete("1.0", tkinter.END)  # Comentado para conservar el texto previo
    while True:
        tok = lexer.token()
        if not tok:
            break
        etiqueta2.insert(
            tkinter.END, f"Encontré un: {tok.type} Lexema: {tok.value}\n")
    etiqueta2.configure(state='disabled')


def LimpiarTerminal():
    etiqueta2.configure(state='normal')
    etiqueta2.delete("1.0", tkinter.END)
    etiqueta2.configure(state='disabled')


ventana = tkinter.Tk()
ventana.geometry("450x400")

marco_botones = tkinter.Frame(ventana)
marco_botones.pack(side="bottom")

etiqueta1 = tkinter.Label(ventana, text="Ingrese la línea")
etiqueta1.pack()

BotonArch = tkinter.Button(marco_botones, text="Abrir Archivo", command=BotonA)
BotonArch.pack(side=tkinter.RIGHT, padx=5)

CajaDeTexto = tkinter.Entry(ventana, width=55)
CajaDeTexto.pack()
# Vincular la pulsación de "Enter" al evento
CajaDeTexto.bind('<Return>', TextoIngresado)

scrollbar = ttk.Scrollbar(ventana)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

etiqueta2 = tkinter.Text(ventana, wrap="word", state='disabled')
etiqueta2.pack(fill=tkinter.BOTH, expand=True)
etiqueta2.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=etiqueta2.yview)

BotonText = tkinter.Button(
    marco_botones, text="Analizar Texto", command=TextoIngresado)
BotonText.pack(side=tkinter.RIGHT, padx=5)

BotonLimpiar = tkinter.Button(
    marco_botones, text="Limpiar terminal", command=LimpiarTerminal)
BotonLimpiar.pack(side=tkinter.RIGHT, padx=5)

ventana.mainloop()
