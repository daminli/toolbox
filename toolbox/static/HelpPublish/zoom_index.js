dictwords = ["introduction 0 10 16 1 10 32 3 10 16",
	"maintain 0 18 24",
	"database 0 10 8 1 10 4 2 18 24",
	"connection 0 10 8 1 10 4",
	"data 0 21 200 1 10 8 2 18 4",
	"source 0 21 200",
	"delete 0 10 4",
	"datasource 0 33 7",
	"test 0 10 4",
	"connect 0 10 2",
	"save 0 10 2",
	"note 0 10 2",
	"just 0 10 1",
	"should 0 10 1",
	"maintained 0 10 1",
	"dba 0 10 1",
	"home 0 10 1 1 10 1 2 10 1 3 10 1",
	"page 0 10 1 1 10 1 2 10 1 3 10 1",
	"http 0 10 1 1 10 1 2 10 1 3 10 1",
	"cost.lenovo.com 0 10 1 1 10 1 2 10 1 3 10 1",
	"execute 0 8 128 1 42 240 2 29 195 3 29 212",
	"sql 0 8 128 1 50 252 2 29 195 3 36 217",
	"data_source.htm 0 6 64",
	".the 1 10 32",
	"function 1 10 32 2 18 3",
	"script 1 60 55",
	"step 1 18 40",
	"create 1 18 16",
	"request 1 18 16 3 10 4",
	"must 1 26 26",
	"reason 1 10 16",
	"why 1 10 16",
	"want 1 10 8",
	"change 1 10 8",
	"manually 1 10 8",
	"this 1 10 8 2 10 2",
	"information 1 10 8 3 10 2",
	"more 1 10 8",
	"than 1 10 8",
	"characters 1 10 8",
	"run 1 18 12 3 40 15",
	"select 1 10 4 3 10 4",
	"input 1 10 4 3 10 8",
	"your 1 26 7 3 10 8",
	"click 1 10 4",
	"button 1 10 4",
	"review 1 10 2 3 18 17",
	"result 1 10 2",
	"notification 1 10 2",
	"add 1 10 2",
	"schema 1 10 2",
	"name 1 10 2",
	"whatever 1 10 2",
	"there 1 10 2",
	"commit 1 18 3",
	"not 1 10 1 2 10 8",
	"system 1 10 1 2 18 16",
	"will 1 10 1 2 18 9",
	"auto 1 10 1",
	"after 1 10 1",
	"finished 1 10 1",
	"execute.htm 1 6 64",
	"background 2 10 32",
	"control 2 10 32",
	"planning 2 26 18",
	"access 2 18 24",
	"reduce 2 10 16",
	"operation 2 10 16",
	"risk 2 10 16",
	"engineers 2 18 10",
	"allowed 2 10 8",
	"application 2 10 8",
	"account 2 10 8",
	"but 2 10 8",
	"also 2 10 4",
	"need 2 10 4",
	"update 2 10 4",
	"some 2 10 4",
	"mid 2 10 4",
	"table 2 10 4",
	"fix 2 10 4",
	"intergration 2 10 4",
	"error 2 10 4",
	"build 2 10 2",
	"logged 2 10 1",
	"history 2 10 1 3 29 216",
	"execute_sql.htm 2 6 64",
	"search 3 26 28",
	"filter 3 10 8",
	"check 3 10 4",
	"log 3 18 5",
	"list 3 10 2",
	"expand 3 10 2",
	"detail 3 18 3",
	"double-click 3 10 1",
	"details 3 10 1",
	"view 3 10 1",
	"history.htm 3 6 64"];
skipwords = ["and",
	"or",
	"the",
	"it",
	"is",
	"an",
	"on",
	"we",
	"us",
	"to",
	"of",
	"has",
	"be",
	"all",
	"for",
	"in",
	"as",
	"so",
	"are",
	"that",
	"can",
	"you",
	"at",
	"its",
	"by",
	"have",
	"with",
	"into"];
var STR_FORM_SEARCHFOR = "Search for:";
var STR_FORM_SUBMIT_BUTTON = "Submit";
var STR_FORM_RESULTS_PER_PAGE = "Results per page:";
var STR_FORM_MATCH = "Match:";
var STR_FORM_ANY_SEARCH_WORDS = "any search words";
var STR_FORM_ALL_SEARCH_WORDS = "all search words";
var STR_NO_QUERY = "No search query entered.";
var STR_RESULTS_FOR = "Search results for:";
var STR_NO_RESULTS = "No results";
var STR_RESULT = "result";
var STR_RESULTS = "results";
var STR_PHRASE_CONTAINS_COMMON_WORDS = "The following phrase contains very common words on this site, resulting in a limited search. Please define a more specific phrase for better results.";
var STR_SKIPPED_FOLLOWING_WORDS = "The following word(s) are in the skip word list and have been omitted from your search:";
var STR_SKIPPED_PHRASE = "Note that you can not search for exact phrases beginning with a skipped word";
var STR_SUMMARY_NO_RESULTS_FOUND = "No results found.";
var STR_SUMMARY_FOUND_CONTAINING_ALL_TERMS = "found containing all search terms.";
var STR_SUMMARY_FOUND_CONTAINING_SOME_TERMS = "found containing some search terms.";
var STR_SUMMARY_FOUND = "found.";
var STR_PAGES_OF_RESULTS = "pages of results.";
var STR_POSSIBLY_GET_MORE_RESULTS = "You can possibly get more results searching for";
var STR_ANY_OF_TERMS = "any of the terms";
var STR_DIDYOUMEAN = "Did you mean:";
var STR_SORTEDBY_RELEVANCE = "Sorted by relevance";
var STR_SORTBY_RELEVANCE = "Sort by relevance";
var STR_SORTBY_DATE = "Sort by date";
var STR_SORTEDBY_DATE = "Sorted by date";
var STR_RESULT_TERMS_MATCHED = "Terms matched:";
var STR_RESULT_SCORE = "Score:";
var STR_RESULT_URL = "URL:";
var STR_RESULT_PAGES = "Results Pages:";
var STR_RESULT_PAGES_PREVIOUS = "Previous";
var STR_RESULT_PAGES_NEXT = "Next";
var STR_FORM_CATEGORY = "Category:";
var STR_FORM_CATEGORY_ALL = "All";
var STR_RESULTS_IN_ALL_CATEGORIES = "in all categories";
var STR_RESULTS_IN_CATEGORY = "in category";
var STR_POWEREDBY = "Search powered by";
var STR_MORETHAN = "More than";
var STR_ALL_CATS = "all categories";
var STR_CAT_SUMMARY = "Refine your search by category:";
var STR_OR = "or";
var STR_RECOMMENDED = "Recommended links";
var STR_SEARCH_TOOK = "Search took";
var STR_SECONDS = "seconds";
var STR_MAX_RESULTS = "You have requested more results than served per query. Please try again with a more precise query.";
