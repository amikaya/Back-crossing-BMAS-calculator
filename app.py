#!/home/eliot/anaconda2/bin/python2.7
import os,sys
import falcon
from falcon_multipart.middleware import MultipartMiddleware
from wsgiref import simple_server

genAccept = ['s1','f1','bc1','bc2','bc3','bc4','bc5','bc6','bc7','bc8']

class Resource(object):
    def on_get(self, req, resp):
        page = 'file_upload.html'
        resp.content_type = "text/html"
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        resp.status = falcon.HTTP_200
        with open( page,'r') as f:
            resp.body = f.read()
	
    def on_options(self, req, resp):
        resp.content_type = "text/plain"
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        resp.status = falcon.HTTP_200

    """def on_post(self, req, resp):
        resp.status = falcon.HTTP_200
        gen = req.get_param['generation']
        fm = req.get_param['fixed_markers']
        print(gen + ' ' + fm + '\n')
        fileIn = req.get_param['datafile']
        resp.body = os.system('python A-B_cal.py -f '+ fileIn +' -g '+gen+' -t ' + fm)"""


class UploadData(object):
    
    def on_get(self, req, resp):
        
        resp.content_type = "text/html"
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        resp.status = falcon.HTTP_200

	
    def on_options(self, req, resp):
        resp.content_type = "text/plain"
        resp.set_header("Access-Control-Allow-Origin", "*")
        resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, **kwargs):
        
        gen = req._params["generation"]
        t = req._params["total_markers"]
        fileIn = req._params["datafile"]
        raw = fileIn.file.read()
        filename = fileIn.filename
        #print(str(len(raw)) + ' ' + gen + ' ' + t + ' ' + filename + '\n')
	
	with open(filename, 'wb') as f:
		f.write(raw)

	html = ''
	os.system("rm tmp.html")

	if filename.endswith('xlsx'):
		try:
			result = os.system('/home/eliot/anaconda2/bin/python A-B_cal.py -f '+ filename +' -g '+gen+' -t ' + t)
			with open('tmp.html', 'r') as f:
			    html = f.read()   
			resp.content_type = "text/html"
			resp.set_header("Access-Control-Allow-Origin", "*")
			resp.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
			resp.status = falcon.HTTP_200
			resp.body = html
		except:
			resp.body = "It have something wrong in your file format, please check it!!"

	else:
		resp.body = "Accept xlsx only!!, please check your file format."


api = application = falcon.API(middleware=[MultipartMiddleware()])
api.req_options.auto_parse_form_urlencoded = True
api.add_route('/', Resource())
api.add_route('/upload', UploadData())

#if __name__ == '__main__':
#    http = simple_server.make_server('192.168.5.82', 5001, app)
#    http.serve_forever()
