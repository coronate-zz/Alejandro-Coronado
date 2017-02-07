%{


#include <map>
using std::map;
#include <string>
using std::string;
#include "errors.h"
%}

%x string_process

%x iniciaComentario

%%

%{
    std::map<std::string, std::string> mapaMacro;
%}



"//"[^\n]*                            {;}
"/*"                                  {BEGIN(iniciaComentario);}
<iniciaComentario>[^*\n]*
<iniciaComentario>[*]+[^*/\n]*
<iniciaComentario>"*"+"/"             BEGIN(INITIAL);
<iniciaComentario>"*"+"/"             BEGIN(INITIAL);


#define" "[A-Z]+" "[^\n]*             {string stringText(yytext);
                                      int spacePos1 = stringText.find(" ");
                                      int spacePos2 = stringText.find(" ", spacePos1 + 1);
                                      string definition = stringText.substr(spacePos1 + 1, spacePos2 - (spacePos1+1));
                                      string valAsigado = stringText.substr(spacePos2 + 1);

                                      mapaMacro.insert(make_pair(definition, valAsigado));
                                      }


#define" "+[^\n]*                     {ReportError::UntermComment();}



#[A-Z]+                                {if(mapaMacro.find(yytext+1)== mapaMacro.end())
                                            ReportError::UntermComment();
                                        else
                                            printf("%s", (*mapaMacro.find(yytext+1)).second.c_str()); //Basta com imprimirlo para que se cambie el texto 
                                        }   







%%

