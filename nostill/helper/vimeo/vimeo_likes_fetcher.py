import sys
import urllib2
import BeautifulSoup as bs
import html5lib
import time
import json
import os

def vimeoLikesFetcher(userName, pageLimit = None):
    """fetches the id numbers from the url's for likes by a given user name in vimeo, 
    with the given page limit if there are any. example usage from the terminal:
    python vimeo_likes_fetcher.py <username> <page limit integer>
    """

    try:
        pageLimit = int(pageLimit)
    except ValueError:
        print "the provided page limit value needs to be of type integer, problem with : %s" % pageLimit
        return

    counter = 1
    path = "http://vimeo.com/%s/likes" %userName
    hrefList = []

    while True:
        print "current path is: %s" % path

        try:
            page = urllib2.urlopen(path)
        except urllib2.HTTPError:
            print "there seems to be a problem with accessing the target path: %s" %path
            return hrefList
    
        soup = bs.BeautifulSoup(page)
        ol = soup.find("ol", {"class":\
            "js-browse_list clearfix browse browse_videos browse_videos_thumbnails kane"})
        links = ol.findAll("a")
        for link in links:
            hrefList.append(link["href"])
        
        if counter == 1:
            path = path +  "/page:2/sort:date"
        else:
            path = "http://vimeo.com/%s/likes/page:%s/sort:date" % (userName, counter+1)

        if counter == pageLimit:
            break

        counter += 1
        time.sleep(0.5)


    return hrefList

def vimeoLikesOutputFile(data, userName, pageLimit = None):
    """outputs the given data in a list file named according to the username and pagelimit values"""

    try:
        pageLimit = int(pageLimit)
    except ValueError:
        print "the provided page limit value needs to be of type integer, problem with : %s" % pageLimit
        return

    if pageLimit:
        fileName = "likes_user-%s_limit-%s.txt" % (userName, pageLimit)
    else:
        fileName = "likes_user-%s.txt" % userName

    filePath = os.path.dirname(__file__)
    output_file_name = os.path.join(filePath, fileName)
    if os.path.exists(output_file_name):
        print "the target output file name already exists at the path"
        return False

    if data:
        with open(output_file_name, 'w') as outfile:
            json.dump(data, outfile)
        print "file %s is created" % output_file_name
    else:
        print "there is no data to be written to a file"
        return False
    
    return True

if __name__ == "__main__":
    run = True
    if len(sys.argv) == 3:
        userName = sys.argv[1]
        pageLimit = sys.argv[2]
    elif len(sys.argv) == 2:
        userName = sys.argv[1]
    else:
        print "please provide, at least, a vimeo username to fetch his/her likes from vimeo"
        run = False

    if run:
        print "username : %s" % userName
        print "page limit: %s" % pageLimit

        likes = vimeoLikesFetcher(userName, pageLimit)
        vimeoLikesOutputFile(likes, userName, pageLimit)


