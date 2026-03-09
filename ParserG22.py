import ply.lex as lex
import ply.yacc as yacc
import re
import os
import codecs
from tkinter import filedialog
from tkinter import Entry, Frame,Tk ,Text, filedialog, ttk, messagebox

tokens = [
    "Article",
    "FinArticle",
    "Itemizedlist",
    "FinItemizedlist",
    "ListItem",
    "FinListItem",
    "Important",
    "FinImportant",
    "Para",
    "FinPara",
    "SimPara",
    "FinSimPara",
    "Emphasis",
    "FinEmphasis",
    "Comment",
    "FinComment",
    "Section",
    "FinSection",
    "Sect1",
    "FinSect1",
    "Info",
    "FinInfo",
    "Title",
    "FinTitle",
    "MediaObject",
    "FinMediaObject",
    "VideoObject",
    "FinVideoObject",
    "VideoData",
    "ImageObject",
    "FinImageObject",
    "ImageData",
    "Abstract",
    "FinAbstract",
    "Address",
    "FinAddress",
    "Street",
    "FinStreet",
    "City",
    "FinCity",
    "State",
    "FinState",
    "Phone",
    "FinPhone",
    "Postcode",
    "FinPostcode",
    "Email",
    "FinEmail",
    "Author",
    "FinAuthor",
    "Name",
    "FinName",
    "Surname",
    "FinSurname",
    "Date",
    "FinDate",
    "Copyright",
    "FinCopyright",
    "Year",
    "FinYear",
    "Holder",
    "FinHolder",
    "Texto",
    "Link",
    "Version",
    "N",
    "Tgroup",
    "FinTgroup",
    "Thead",
    "FinThead",
    "Tfoot",
    "FinTfoot",
    "Tbody",
    "FinTbody",
    "Row",
    "FinRow",
    "Entry",
    "FinEntry",
    "Entrytbl",
    "FinEntrytbl",
    "Informaltable",
    "FinInformaltable"
]


BanInfo = False 
banderal = 0
PTitle = True
ilBand = False


def t_Article(t):
    r'<article>'
    global textocreado
    textocreado+="<body>\n"
    return t

def t_FinArticle(t):
    r'</article>'
    global textocreado
    textocreado+="</body>\n</html>\n"
    return t

def t_Itemizedlist(t):
    r'<itemizedlist>'
    global textocreado, PTitle, BanInfo, ilBand
    ilBand = True
    if not BanInfo:
        PTitle = False
    textocreado+="<ul>\n"
    return t

def t_FinItemizedlist(t):
    r'</itemizedlist>'
    global textocreado, ilBand
    ilBand = False
    textocreado+="</ul>\n"
    return t

def t_ListItem(t):
    r'<listitem>'
    return t

def t_FinListItem(t):
    r'</listitem>'
    return t

def t_Important(t):
    r'<important>'
    global textocreado, BanInfo, PTitle
    if not BanInfo:
        PTitle = False
    
    textocreado+='<div style="background-color:red;color:white;"><strong>'
    return t

def t_FinImportant(t):
    r'</important>'
    global textocreado
    textocreado+="</strong>\n</div>\n"
    return t

def t_Para(t):
    r'<para>'
    global textocreado, PTitle, BanInfo, ilBand
    
    if ilBand:
        textocreado+="\t<li>"
    elif not BanInfo:
        PTitle = False
        textocreado+="<p>"
    return t

def t_FinPara(t):
    r'</para>'
    global textocreado, BanInfo, ilBand
    
    if ilBand:
        textocreado+="</li>\n"
    elif not BanInfo:
        textocreado+="</p>\n"
    else:
        textocreado+=" "
    
    return t
def t_SimPara(t):
    r'<simpara>'
    global textocreado, BanInfo, PTitle, ilBand
    
    if ilBand:
       textocreado+="\t<li>"
    elif not BanInfo:
        PTitle = False
        textocreado+="<p>"
    return t

def t_FinSimPara(t):
    r'</simpara>'
    global textocreado, BanInfo
    
    if ilBand:
       textocreado+="</li>\n"
    elif not BanInfo:
        textocreado+="</p>\n"
    else:
        textocreado+=" "
    return t

def t_Emphasis(t):
    r'<emphasis>'
    global textocreado
    textocreado+="<em>"
    return t

def t_FinEmphasis(t):
    r'</emphasis>'
    global textocreado, banderal
    textocreado+="</em>\n"
    
    if banderal == 1:
         textocreado+="</a>"
         banderal = 0
    return t

def t_Comment(t):
    r'<comment>'
    global textocreado, PTitle, BanInfo, ilBand
    if not BanInfo:
        PTitle = False
    textocreado+="<!--"
    
    if ilBand:
       textocreado+="\t<li>"
    else:
        textocreado+="<!--"
    return t

def t_FinComment(t):
    r'</comment>'
    global textocreado, banderal, ilBand
    
    textocreado+="-->"
    if banderal == 1:
        textocreado+="</a>"
        banderal = 0

    if ilBand:
        textocreado+="</li>\n"
    return t



def t_Section(t):
    r'<section>'
    global textocreado
    textocreado+=str(t.value+"\n")
    return t

def t_FinSection(t):
    r'</section>'
    global textocreado
    textocreado+=str(t.value+"\n")
    return t

def t_Sect1(t):
    r'<sect1>'
    global textocreado
    textocreado+="<section>\n"
    return t

def t_FinSect1(t):
    r'</sect1>'
    global textocreado
    textocreado+="</section>\n"
    return t

def t_Info(t):
    r'<info>'
    global textocreado, BanInfo
    BanInfo = True
    textocreado+='<p style="background-color:green;color:white;font-size:8pt">'

    return t

def t_FinInfo(t):
    r'</info>'
    global textocreado, BanInfo
    BanInfo = False
    textocreado+="</p>\n"
    return t

def t_Title(t):
    r'<title>'
    global textocreado, BanInfo, PTitle
    
    if not BanInfo:
        if PTitle:
            textocreado+="<h1>"
        else:
            textocreado+="<h2>"
    return t

def t_FinTitle(t):
    r'</title>'
    global textocreado, BanInfo, PTitle
    if not BanInfo:
        if PTitle:
            textocreado+="</h1>\n"
        else:
            textocreado+="</h2>\n"
    else:
        textocreado+=" "
    return t

def t_MediaObject(t):
    r'<mediaobject>'
    global textocreado, PTitle, BanInfo
    if not BanInfo:
        PTitle = False
    textocreado+="<div>\n"
    return t

def t_FinMediaObject(t):
    r'</mediaobject>'
    global textocreado
    textocreado+="</div>\n"
    return t

def t_VideoObject(t):
    r'<videoobject>'
    return t

def t_FinVideoObject(t):
    r'</videoobject>'
    return t

def t_VideoData(t):
    r'<videodata\ fileref="(http://|https://|ftp://|ftps://)([a-z-A-Z]+|\&|[0-9]|\.|\/|\#|\=|\?|\_|\:|\-)+"\ />'
    global textocreado
    
    Aux = str(t.value)
    
    if "www.youtube.com" in Aux.lower():
        
        Aux = Aux.replace('<videodata fileref','<iframe loading="lazy" src')
        Aux=Aux.replace("https://www.youtube.com/watch?v=","https://www.youtube.com/embed/")
        E_Reg = r'&.*>'
        Nuevo_Valor = '?enablejsapi=1&amp;rel=0" width="320" height="240" frameborder="0" allowfullscreen="allowfullscreen"></iframe>\n'
        Aux = re.sub(E_Reg, Nuevo_Valor, Aux)
    else:
        Aux = Aux.replace('<videodata fileref','<iframe loading="lazy" src')
        Aux = Aux.replace('/>',' width="320" height="240" frameborder="0" allowfullscreen="allowfullscreen" id="player1"></iframe>\n')
    
    textocreado+=Aux
    return t

def t_ImageObject(t):
    r'<imageobject>'
    return t

def t_FinImageObject(t):
    r'</imageobject>'
    global textocreado
    textocreado+="</img>\n"
    return t

def t_ImageData(t):
    r'<imagedata\ fileref="(http://|https://|ftp://|ftps://)?(\w+|\.*|\/*|\#*|\=*|\?*|\:*|\(*|\)*|\&*|\-*|\_*)+"\ />'
    global textocreado
    textocreado+=str(t.value)
    textocreado = textocreado.replace('<imagedata fileref','<img width="320" height="240" src')
    textocreado = textocreado.replace("/>",">")
    return t

def t_Abstract(t):
    r'<abstract>'
    global PTitle, BanInfo
    if not BanInfo:
        PTitle = False
    return t

def t_FinAbstract(t):
    r'</abstract>'
    return t

def t_Address(t):
    r'<address>'
    global PTitle, BanInfo
    if not BanInfo:
        PTitle = False
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
    global textocreado, BanInfo
    if not BanInfo:
        textocreado+='<a href="'
    return t

def t_FinEmail(t):
    r'</email>'
    global textocreado,banderal, BanInfo
    if not BanInfo:
        textocreado+='">email</a>\n'
    
    if banderal == 1:
         textocreado+="</a>"
         banderal = 0
    return t

def t_Author(t):
    r'<author>'
    return t

def t_FinAuthor(t):
    r'</author>'
    global textocreado,banderal
    
    if banderal == 1:
         textocreado+="</a>"
         banderal = 0
    return t

def t_Name(t):
    r'<firstname>'
    return t

def t_FinName(t):
    r'</firstname>'
    global textocreado
    textocreado+= " "
    return t

def t_Surname(t):
    r'<surname>'
    global textocreado
    textocreado+=" "
    return t

def t_FinSurname(t):
    r'</surname>'
    global textocreado
    textocreado+= " "
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
    global textocreado
    textocreado+=' '
    return t

def t_Link(t):
    r'<link\ xlink:href="(http://|https://|ftp://|ftps://)(\w+\.*\/*\#*\=*\?*\:*\-*)+"\ />'
    global textocreado, banderal
    textocreado+=str(t.value)
    textocreado = textocreado.replace("<link xlink:href=","<a href=")
    textocreado = textocreado.replace(" />",">")
    banderal = 1
    return t

def t_Texto(t):
    r'([a-zA-Z]+|ñ+|[0-9]+|á|é|í|ó|ú|Á|É|Í|Ó|Ú|\-|_|\#|&|\(|\)|\?|\¿|!|¡|\,|\=|\.|/+|"|;|:|\ +)+'
    global textocreado, banderal
    textocreado+= str(t.value)
    if banderal == 1:
         textocreado+="</a>"
         banderal = 0
    return t

def t_Version(t):
    r'(<!DOCTYPE\s?article>|<\?xml\s?version="1.0"\s?encoding="UTF-8"\?>|<\?xml\s?version="1.1"\s?encoding="UTF-8"\?>)'
    global textocreado
    textocreado+="<!DOCTYPE html>\n<html>\n"
    return t

def t_N(t):
    r'[0-9]'
    global textocreado
    textocreado+=str(t.value)
    return t

def t_Tgroup(t):
    r'<tgroup>'
    global textocreado
    textocreado+="<colgroup>\n"
    return t

def t_FinTgroup(t):
    r'</tgroup>'
    global textocreado
    textocreado+="</colgroup>\n"
    return t

def t_Thead(t):
    r'<thead>'
    global textocreado
    textocreado+=str(t.value+"\n")
    return t

def t_FinThead(t):
    r'</thead>'
    global textocreado
    textocreado+="</thead>\n"
    return t

def t_Tfoot(t):
    r'<tfoot>'
    global textocreado
    textocreado+=str(t.value+"\n")
    return t

def t_FinTfoot(t):
    r'</tfoot>'
    global textocreado
    textocreado+="</tfoot>\n"
    return t

def t_Tbody(t):
    r'<tbody>'
    global textocreado
    textocreado+=str("\t"+t.value+"\n")
    return t

def t_FinTbody(t):
    r'</tbody>'
    global textocreado
    textocreado+="\t</tbody>\n"
    return t

def t_Row(t):
    r'<row>'
    global textocreado
    textocreado+="\t\t<tr>\n"
    return t

def t_FinRow(t):
    r'</row>'
    global textocreado
    textocreado+="\t\t</tr>\n"
    return t

def t_Entry(t):
    r'<entry>'
    global textocreado
    textocreado+="\t\t\t<td>"
    return t

def t_FinEntry(t):
    r'</entry>'
    global textocreado
    textocreado+="</td>\n"
    return t

def t_Entrytbl(t):
    r'<entrytbl>'
    global textocreado
    textocreado+="<table>\n"
    return t

def t_FinEntrytbl(t):
    r'</entrytbl>'
    global textocreado
    textocreado+="</table>\n"
    return t

def t_Informaltable(t):
    r'<informaltable>'
    global textocreado, PTitle, BanInfo
    if not BanInfo:
        PTitle = False
    textocreado+="<table>\n"
    return t

def t_FinInformaltable(t):
    r'</informaltable>'
    global textocreado
    textocreado+="</table>\n"
    return t

def t_newline(t):
    r'\n+'
    global lineas
    t.lexer.lineno += len(t.value)
    
t_ignore = ' '

def t_error(t):
    t.lexer.skip(1)

lexer = lex.lex()

def p_sigma(p):
    '''sigma : VERSION'''
    
def p_VERSION(p):
    '''VERSION : Version Article ARTICLE FinArticle'''
    
def p_ARTICLE(p):
    '''ARTICLE : INFO TITLE OTRO SECTSS
    | TITLE OTRO SECTSS
    | INFO TITLE OTRO
    | TITLE OTRO
    | INFO OTRO SECTSS
    | OTRO SECTSS
    | INFO OTRO
    | OTRO'''
    
def p_INFO(p):
    '''INFO : Info IN_INFO FinInfo'''
    
def p_IN_INFO(p):
    '''IN_INFO : IN_INFO IN_INFO
    | MEDIAOBJECT 
    | ABSTRACT 
    | ADDRESS 
    | AUTHOR 
    | DATE 
    | COPYRIGHT
    | TITLE'''
    
def p_TITLE(p):
    '''TITLE : Title IN_TITLE FinTitle'''
    
def p_IN_TITLE(p):
    '''IN_TITLE : IN_TITLE IN_TITLE
    | Texto
    | EMPHASIS
    | LINK
    | EMAIL'''
    
def p_OTRO(p):
    '''OTRO : OTRO OTRO
    | ITEMIZEDLIST
    | IMPORTANT
    | PARA
    | SIMPARA
    | ADDRESS
    | MEDIAOBJECT
    | INFORMALTABLE
    | COMMENT
    | ABSTRACT'''
    
def p_SECTSS(p):
    '''SECTSS : SECTSS SECTSS
    | SECT 
    | SIMPLESECT'''
    
def p_SECT(p):
    '''SECT : Section IN_SECT FinSection'''
    
def p_IN_SECT(p):
    '''IN_SECT : INFO TITLE OTRO SECTSS
    | INFO OTRO SECTSS
    | TITLE OTRO SECTSS
    | OTRO SECTSS
    | INFO TITLE OTRO
    | INFO OTRO
    | TITLE OTRO
    | OTRO'''
    
def p_SIMPLESECT(p):
    '''SIMPLESECT : Sect1 IN_SIM_SECT FinSect1'''
    
def p_IN_SIM_SECT(p):
    '''IN_SIM_SECT : INFO TITLE OTRO
    | INFO OTRO
    | TITLE OTRO
    | OTRO'''
    
def p_ITEMIZEDLIST(p):
    '''ITEMIZEDLIST : Itemizedlist LISTITEM FinItemizedlist'''
    
def p_LISTITEM(p):
    '''LISTITEM : LISTITEM LISTITEM
    | ListItem OTRO FinListItem'''
    
def p_IMPORTANT(p):
    '''IMPORTANT : Important TITLE OTRO FinImportant
    | Important OTRO FinImportant'''
    
def p_PARA(p):
    '''PARA : Para IN_PARA FinPara'''
    
def p_IN_PARA(p):
    '''IN_PARA : IN_PARA IN_PARA
    | Texto
    | EMPHASIS
    | LINK
    | EMAIL
    | AUTHOR
    | COMMENT
    | ITEMIZEDLIST
    | IMPORTANT
    | ADDRESS
    | MEDIAOBJECT
    | INFORMALTABLE'''
    
def p_SIMPARA(p):
    '''SIMPARA : SimPara IN_SIMPARA FinSimPara'''
    
def p_IN_SIMPARA(p):
    '''IN_SIMPARA : M'''
    
def p_M(p):
    '''M : M M
    | Texto
    | EMPHASIS
    | LINK
    | EMAIL
    | AUTHOR
    | COMMENT'''
    
def p_ADDRESS(p):
    '''ADDRESS : Address IN_ADDRESS FinAddress
    | Address FinAddress'''
    
def p_IN_ADDRESS(p):
    '''IN_ADDRESS : IN_ADDRESS  IN_ADDRESS
    | Texto
    | STREET 
    | CITY
    | STATE
    | PHONE
    | EMAIL
    | POSTCODE'''
    
def p_MEDIAOBJECT(p):
    '''MEDIAOBJECT : MediaObject IN_MEDIAOBJECT FinMediaObject'''
    
def p_IN_MEDIAOBJECT(p):
    '''IN_MEDIAOBJECT : INFO VID_IM
    | VID_IM'''
    
def p_VID_IM(p):
    '''VID_IM : VID_IM VID_IM
    | VideoObject VIDEOOBJECT FinVideoObject
    | ImageObject IMAGEOBJECT FinImageObject'''
    
def p_VIDEOOBJECT(p):
    '''VIDEOOBJECT : INFO VideoData
    | VideoData'''
    
def p_IMAGEOBJECT(p):
    '''IMAGEOBJECT : INFO ImageData
    | ImageData'''
    
def p_INFORMALTABLE(p):
    '''INFORMALTABLE : Informaltable IN_INFTABLE FinInformaltable'''
    
def p_IN_INFTABLE(p):
    '''IN_INFTABLE : IN_INFTABLE TGROUP
    | IN_INFTABLE MEDIAOBJECT
    | TGROUP MEDIAOBJECT
    | TGROUP 
    | MEDIAOBJECT TGROUP'''
    
def p_TGROUP(p):
    '''TGROUP : Tgroup THEAD TFOOT TBODY FinTgroup
    | Tgroup TFOOT TBODY FinTgroup
    | Tgroup THEAD TBODY FinTgroup
    | Tgroup TBODY FinTgroup'''

def p_THEAD(p):
    '''THEAD : Thead ROW FinThead'''
    
def p_TFOOT(p):
    '''TFOOT : Tfoot ROW FinTfoot'''
    
def p_TBODY(p):
    '''TBODY : Tbody ROW FinTbody'''
    
def p_ROW(p):
    '''ROW : ROW ROW
    | Row IN_ROW FinRow'''
    
def p_IN_ROW(p):
    '''IN_ROW : IN_ROW IN_ROW
    | ENTRY
    | ENTRYTBL'''
  
def p_ENTRYTBL(p):
    '''ENTRYTBL : Entrytbl THEAD TBODY FinEntrytbl
    | Entrytbl TBODY FinEntrytbl'''
  
def p_ENTRY(p):
    '''ENTRY : Entry IN_ENTRY FinEntry'''

def p_IN_ENTRY(p):
    '''IN_ENTRY : IN_ENTRY IN_ENTRY 
    | Texto
    | ITEMIZEDLIST
    | IMPORTANT
    | PARA
    | SIMPARA
    | ADDRESS
    | MEDIAOBJECT
    | COMMENT
    | ABSTRACT'''
    
def p_COMMENT(p):
    '''COMMENT : Comment M FinComment'''

def p_ABSTRACT(p):
    '''ABSTRACT : Abstract IN_ABSTRACT FinAbstract'''
    
def p_IN_ABSTRACT(p):
    '''IN_ABSTRACT : TITLE PARRAFOS
    | PARRAFOS'''
    
def p_PARAS(p):
    '''PARRAFOS : PARRAFOS PARRAFOS
    | PARA
    | SIMPARA'''
    
def p_AUTHOR(p):
    '''AUTHOR : Author PERSONNAME FinAuthor'''
    
def p_PERSONNAME(p):
    '''PERSONNAME : PERSONNAME PERSONNAME
    | FIRSTNAME
    | SURNAME'''
    
def p_FIRSTNAME(p):
    '''FIRSTNAME : Name DATOS FinName'''
    
def p_SURNAME(p):
    '''SURNAME : Surname DATOS FinSurname'''
    
def p_DATOS(p):
    '''DATOS : DATOS DATOS
    | Texto
    | LINK
    | EMPHASIS
    | COMMENT'''
    
def p_COPYRIGHT(p):
    '''COPYRIGHT : Copyright IN_COPYRIGHT FinCopyright'''
    
def p_IN_COPYRIGHT(p):
    '''IN_COPYRIGHT : YEAR HOLDER
    | YEAR'''
    
def p_YEAR(p):
    '''YEAR : Year DATOS FinYear YEAR 
    | Year DATOS FinYear'''
    
def p_HOLDER(p):
    '''HOLDER : Holder DATOS FinHolder HOLDER
    | Holder DATOS FinHolder'''
    
def p_EMPHASIS(p):
    '''EMPHASIS : Emphasis M FinEmphasis'''

def p_LINK(p):
    '''LINK : Link M'''
    
def p_STREET(p):
    '''STREET : Street DATOS FinStreet'''
    
def p_CITY(p):
    '''CITY : City DATOS FinCity'''
    
def p_STATE(p):
    '''STATE : State DATOS FinState'''
    
def p_PHONE(p):
    '''PHONE : Phone DATOS FinPhone'''
    
def p_EMAIL(p):
   '''EMAIL : Email DATOS FinEmail'''

def p_DATE(p):
    '''DATE : Date DATOS FinDate'''

def p_POSTCODE(p):
    '''POSTCODE : Postcode N N N N FinPostcode'''
    
def p_error(p):
    global correcto
    correcto=1
    pantalla1.configure(state="normal")
    pantalla1.insert('1.0', "Error en la línea "+str(p.lineno)+"\nVerifique la cadena "+str(p.value)+"\n\n")
    pantalla1.configure(state="disabled")

parser = yacc.yacc()

textocreado = ""
correcto=0

codigo = ""
Arch = None

#Funcion interactuar con caja de texto superior
def Pantalla():
    global codigo, correcto, textocreado, Arch

    pantalla1.configure(state="normal")
    pantalla1.delete("1.0", "end")
    pantalla1.configure(state="disabled")

    codigo = pantalla.get("1.0", 'end-1c')
    lexer.lineno = 1
    correcto = 0

    parser.parse(codigo)

    if codigo != "" and correcto == 0:
        respuesta = messagebox.askquestion("Resultado", "Compilación exitosa.\n¿Desea guardar el código como archivo HTML?", icon="question")

        if respuesta == 'yes':
            if textocreado != "" and correcto == 0:
                if Arch != None:
                    messagebox.showinfo("Resultado", "Elija el lugar para guardar el archivo ;)")
                    file_path = filedialog.asksaveasfilename(initialfile=os.path.splitext(os.path.basename(Arch.name))[0], defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
                    if file_path:
                        with open(file_path, "w") as archivo_guardado:
                            archivo_guardado.write(textocreado)
                            messagebox.showinfo("Resultado", "Archivo guardado correctamente como HTML.")
                else:
                    messagebox.showinfo("Resultado", "Asigne un nombre y elija el lugar para guardar el archivo ;)")
                    file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("Archivos HTML", "*.html")])
                    if file_path:
                        with open(file_path, "w") as archivo_guardado:
                            archivo_guardado.write(textocreado)
                            messagebox.showinfo("Resultado", "Archivo guardado correctamente como HTML.")
    else:
        textocreado=""
        
#Funcion abrir archivo
def OpenArch():
    global Arch
    tipos_archivo = [("", "*.txt *.xml")]
    Archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=tipos_archivo)
    Arch = codecs.open(Archivo, "r", encoding="utf-8")
    a = Arch.read()
    pantalla.delete("1.0", "end")
    pantalla.insert('1.0', a)

ventana_principal=Tk()
ventana=Frame(ventana_principal)
ventana_principal.title("Parser G-22")
ventana_principal.resizable(0, 0)

#Caja de texto superior
pantalla= Entry(ventana)
pantalla= Text( width=100, height=20, font=("Helvetica", 10))

#Ubicar caja
pantalla.grid (row=1, column=0, columnspan=4,padx=10,pady=10)

#Caja de inferior
pantalla1= Entry(ventana)
pantalla1= Text(width=100, height=10, font=("Helvetica", 10))
pantalla1.configure(state="disabled")

#Ubicar caja
pantalla1.grid (row=2, column=0, columnspan=4,padx=10,pady=10)

#Boton Abrir archivo
ventana.boton_abrirarchivo= ttk.Button(text="Abrir Archivo", command=OpenArch, width=20).grid(row=3,column=0,pady=15,columnspan=2)

#Boton compilar
ventana.boton_compilar= ttk.Button(text="Compilar", command=Pantalla, width=20).grid(row=3, column=1,padx=10,pady=15,columnspan=2)

#Boton Exit
ventana.boton_cerrar= ttk.Button(ventana_principal,text='Cerrar',command=lambda: ventana_principal.quit(), width=20).grid(row=3, column=2,pady=15, columnspan=2)

ventana_principal.mainloop()


