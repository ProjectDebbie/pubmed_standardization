import sys
import os
import argparse
import gzip
import xml.etree.ElementTree as ET
import configparser
import codecs

import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

parser=argparse.ArgumentParser()
parser.add_argument('-i', help='Input Directory')
parser.add_argument('-o', help='Output Directory')
args=parser.parse_args()
parameters={}
if __name__ == '__main__':
    import pubmed_standardization
    parameters = pubmed_standardization.ReadParameters(args)     
    pubmed_standardization.Main(parameters)

def Main(parameters):
    standardization_output= parameters['output']
    standardization_input = parameters['input']
    if not os.path.exists(standardization_output):
        os.makedirs(standardization_output)
    unzip(standardization_input)
    standardization(standardization_input,standardization_output)

def ReadParameters(args):
    parameters_error=False
    parameters_obligation=False
    if(args.i!=None):
        parameters['input']=args.i
    elif (parameters_obligation):
        print ("No input directory provided")
        parameters_error=False
    if(args.o!=None):
        parameters['output']=args.o
    elif (parameters_obligation):
        print ("No output directory provided")
        parameters_error=False
    if(parameters_error):
        print("Please send the correct parameters.  You can type for --help ")
        sys.exit(1)
    return parameters

def unzip(standardization_input):
    logging.info("Unzip Input Directory " + standardization_input)
    ids_list=[]
    if(os.path.isfile(standardization_input+"/list_files_unziped.dat")):
        with open(standardization_input+"/list_files_unziped.dat",'r') as ids:
            for line in ids:
                ids_list.append(line.replace("\n",""))
        ids.close()
    
    pubMedRetrievals=[]
    if os.path.exists(standardization_input):
        subs = [os.path.join(standardization_input, f) for f in os.listdir(standardization_input) if os.path.isdir(os.path.join(standardization_input, f))]
        for sub in subs:
            onlyfiles = [os.path.join(os.path.join(sub, f)) for f in os.listdir(sub) if (os.path.isfile(os.path.join(sub, f)) & f.endswith('.xml.gz') & (os.path.basename(f) not in ids_list))]
            pubMedRetrievals = pubMedRetrievals + onlyfiles   
    with open(standardization_input+"/list_files_unziped.dat",'a') as list_files_unziped:
        for pubMedRetrieval in pubMedRetrievals:
            file=pubMedRetrieval
            xml_file_path = file + ".xml"
            if os.path.isfile(file):
                with open(xml_file_path,'wb') as xml_file:
                    with gzip.open(file, 'rb') as f:    
                        file_content = f.read()
                        xml_file.write(file_content)
                        xml_file.flush()
                        xml_file.close()
                        logging.info("unziped   : " + file)
                        list_files_unziped.write(os.path.basename(file)+"\n")
                        list_files_unziped.flush()
            else:
                print ("The file " + file + " not exist, please review and download again ") 
    list_files_unziped.close()    
    logging.info("Unzip End ")      
                       
def standardization(standardization_input, standardization_output):
    logging.info("Standardization Input Directory " + standardization_input)
    ids_list=[]
    if(os.path.isfile(standardization_input+"/debbie_standardization_list_files_processed.dat")):
        with open(standardization_input+"/debbie_standardization_list_files_processed.dat",'r') as ids:
            for line in ids:
                ids_list.append(line.replace("\n",""))
        ids.close()
    pubMedRetrievals=[]
    if os.path.exists(standardization_input):
        subs = [os.path.join(standardization_input, f) for f in os.listdir(standardization_input) if os.path.isdir(os.path.join(standardization_input, f))]
        for sub in subs:
            onlyfiles = [os.path.join(sub, f) for f in os.listdir(sub) if (os.path.isfile(os.path.join(sub, f)) & f.endswith('.xml') & (os.path.basename(f) not in ids_list))]
            pubMedRetrievals = pubMedRetrievals + onlyfiles
    with open(standardization_input+"/debbie_standardization_list_files_processed.dat",'a') as list_files_standardized:
        for pubMedRetrieval in pubMedRetrievals:
            if not os.path.exists(standardization_output):
                os.makedirs(standardization_output)
            xml_file_path=pubMedRetrieval
            if os.path.isfile(xml_file_path):
                file_name = os.path.basename(xml_file_path)
                with open(xml_file_path,'r') as xml_file:    
                    txt_file_path=  standardization_output + "/" + file_name + "/"
                    if not os.path.exists(txt_file_path):
                        os.makedirs(txt_file_path)
                    logging.info("Parsing: " + xml_file_path)
                    docXml = ET.parse(xml_file)
                    for article in docXml.findall("PubmedArticle"):
                        try: 
                            year = "NA"
                            month = ''
                            title = ''
                            pmid = article.find("MedlineCitation").find("PMID").text
                            article_xml = article.find("MedlineCitation").find("Article")
                            try: year = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('Year').text
                            except Exception: year ='NA'
                            try: month = article_xml.find('Journal').find('JournalIssue').find('PubDate').find('Month').text
                            except Exception: month=''
                            abstract_xml = article_xml.find("Abstract")
                            if(abstract_xml is not None):
                                abstract = readAbstract(abstract_xml)
                                title = readTitle(article_xml.find('ArticleTitle'))
                                if(abstract!=''):
                                    with codecs.open(txt_file_path +  pmid + '.txt', 'w',encoding='utf8') as txt_file:
                                        txt_file.write(str(year) + ' ' + str(month) + '\n' + remove_invalid_characters(title) + '\n' + remove_invalid_characters(abstract) + '\n')
                                        #txt_file.write(remove_invalid_characters(abstract) + "\n")
                                        txt_file.flush()
                                        txt_file.close()    
                        except Exception as inst:
                            logging.error("Error generation data set for classification " + pmid)
                logging.info("Standardization: " + os.path.basename(xml_file_path))
                list_files_standardized.write(os.path.basename(xml_file_path)+"\n")
                list_files_standardized.flush()
    list_files_standardized.close()   
    logging.info("Standardization End")


def remove_invalid_characters(text):
    text = text.replace("\n"," ").replace("\t"," ").replace("\r"," ")    
    return text

def readTitle(title_xml):
    if(title_xml!=None):
        title=''.join(title_xml.itertext())
        return title
    return ''

def readAbstract(abstract_xml):
    abstract = []
    for abstractText in abstract_xml.findall("AbstractText"):
        abstract.append("".join(abstractText.itertext()))
    abstract = " ".join(abstract)  
    return abstract
                
                      
                                