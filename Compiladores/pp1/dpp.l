%{


#include <map>
using std::map;
using std::pair;
using std::make_pair;
#include <string>
using std::string;
#include "errors.h"
%}

%x string_process

%x iniciaComentario

%%

%{
    int line_num = 1;
    std::map<std::string, std::string> mapaMacro;
%}

\n   ++line_num;
 
\"                 BEGIN(string_process);  
<string_process>\n BEGIN(INITIAL);   ++line_num;
<string_process>\" BEGIN(INITIAL);  


\"#define" "[A-Z]+" "[^\n]* 
#define" "[A-Z]+" "[^\n]*             {string stringText(yytext);
                                      int spacePos1 = stringText.find(" ");
                                      int spacePos2 = stringText.find(" ", spacePos1 + 1);
                                      string definition = stringText.substr(spacePos1 + 1, spacePos2 - (spacePos1+1));
                                      string valAsigado = stringText.substr(spacePos2 + 1);

                                      mapaMacro.insert(make_pair(definition, valAsigado));
                                      }


#define" "+[^\n]*                     {ReportError::InvalidDirective(line_num);}



#[A-Z]+                                {auto replace_it = mapaMacro.find(yytext+1);
                                        if(replace_it == mapaMacro.end())
                                            ReportError::InvalidDirective(line_num);
                                        else
                                            printf("%s", (*replace_it).second.c_str()); //Basta com imprimirlo para que se cambie el texto 
                                        }   



#[[:alpha:]]*                       {ReportError::InvalidDirective(line_num);}



"//"[^\n]*                      {;}
"/*"                            {BEGIN(iniciaComentario);}
<iniciaComentario>[^*\n]*
<iniciaComentario>[*]+[^*/\n]*
<iniciaComentario>\n             ++line_num;
<iniciaComentario>"*"+"/"      BEGIN(INITIAL);
%%