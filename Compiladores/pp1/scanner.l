
%{



#include <string.h>
#include "stdio.h"
#include "scanner.h"
#include "utility.h" // for PrintDebug()
#include "errors.h"


/* Global variable: yylval
 * -----------------------
 * This global variable is how we get attribute information about the token
*/

/* Global variable: yylloc
 * -----------------------
 * This global variable is how we get position information about the token
 */

/* Macro: YY_USER_ACTION 
 * ---------------------
 * This flex built-in macro can be defined to provide an action which is
 * always executed prior to any matched rule's action. 
 */


YYSTYPE yylval;  // manually declared for pp1, later Yacc provides
struct yyltype yylloc; // manually dclared for pp1, later Yacc provides
static void DoBeforeEachAction(); 
#define YY_USER_ACTION DoBeforeEachAction();



%}



%x stringConstant

%%             /* BEGIN RULES SECTION */




[ ]+            { ; }
(\n)			{yylloc.first_line=yylloc.first_line+1;
				 yylloc.last_column=0;}




"void"			{ return T_Void;}
"int"			{return T_Int; }
"double"		{return T_Double; }
"bool"			{return T_Bool; }
"string"		{return T_String;}
"class"			{return T_Class;}
"interface"		{return T_Interface;}
"null"			{return T_Null;}
"this"			{return T_This;}
"extends"		{return T_Extends;}
"implements"	{return T_Implements;}
"for"			{return T_For;}
"while"			{return T_While;}
"if"			{return T_If;}
"else"			{return T_Else;}
"return"		{return T_Return;}
"break"			{return T_Break;}
"New"			{return T_New;}
"NewArray"		{return T_NewArray;}


(\+)			{return yytext[0];}
(\-)			{return yytext[0];}
(\*)			{return yytext[0];}
(\/)			{return yytext[0];}
(\%)			{return yytext[0];}
(\!)			{return yytext[0];}
(\;)			{return yytext[0];}
(\,)			{return yytext[0];}
(\.)			{return yytext[0];}
(\[|\])			{return yytext[0];}
(\(|\))			{return yytext[0];}
(\{|\})			{return yytext[0];}
(\=)			{return yytext[0];}
(\>)			{return yytext[0];}
(\<)			{return yytext[0];}

(">=")			{return T_GreaterEqual;}
("<=")			{return T_LessEqual;}
("==")			{return T_Equal;}
("!=")			{return T_NotEqual;}
("&&")			{return T_And;}
("||")			{return T_Or;}

([0-9]+)										{yylval.integerConstant=atoi(yytext);
				 							 	 return T_IntConstant;}	

("0X"|"0x")([0-9a-fA-F]+)						{yylval.integerConstant=strtol(yytext, NULL, 16);
				 							 	 return T_IntConstant;}	

("true"|"false")								{yylval.boolConstant=(yytext[0] == 't' );
				 	 							 return T_BoolConstant;}

([0-9]+\.[0-9]*)E("+"|"-")([0-9]+) 				{yylval.doubleConstant=atof(yytext);
				 							 	 return T_DoubleConstant; }


([0-9]+\.[0-9]*)								{yylval.doubleConstant=atof(yytext);
			 				 	 				return T_DoubleConstant;}





\"												{BEGIN(stringConstant);}

<stringConstant>([A-Za-z][A-Za-z0-9_])			{strcpy(yylval.identifier, yytext);
								 				return T_StringConstant;}

<stringConstant>(\")							{BEGIN(INITIAL);}

([A-Za-z][A-Za-z0-9_]{0,30})					{strcpy(yylval.identifier, yytext);
												 				return T_Identifier;}	

([A-Za-z][A-Za-z0-9_]{32,})						{ReportError::LongIdentifier(NULL,"e");}


.                   							{ReportError::UnrecogChar(&yylloc, yytext[0]); }
%%




/* Function: InitScanner
 * ---------------------
 * This function will be called before any calls to yylex().  It is designed
 * to give you an opportunity to do anything that must be done to initialize
 * the scanner (set global variables, configure starting state, etc.). One
 * thing it already does for you is assign the value of the global variable
 * yy_flex_debug that controls whether flex prints debugging information
 * about each token and what rule was matched. If set to false, no information
 * is printed. Setting it to true will give you a running trail that might
 * be helpful when debugging your scanner. Please be sure the variable is
 * set to false when submitting your final version.
 */
void InitScanner()
{
    PrintDebug("lex", "Initializing scanner");
    yy_flex_debug = false;
    printf("\nInitScanner Ejecucion\n");
    yylloc.last_column = 0;
    yylloc.first_line = 1;


}


/* Function: DoBeforeEachAction()
 * ------------------------------
 * This function is installed as the YY_USER_ACTION. This is a place
 * to group code common to all actions.
 */
static void DoBeforeEachAction()
{


    yylloc.first_column = yylloc.last_column + 1;
  	yylloc.last_column += yyleng;

}






