#!/usr/bin/env ruby

# sqid -- SQL Injection Digger
#         http://sqid.rubyforge.org
#
# Copyright (C) Metaeye Security Group <contact@metaeye.org>
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation; version 2.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# A copy of the GNU GPL is available as /usr/doc/copyright/GPL on Debian
# systems, or on the World Wide Web at http://www.gnu.org/copyleft/gpl.html
# You can also obtain it by writing to the Free Software Foundation, Inc.,
# 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA

# program name and version
$program = ["sqid" , "0.3"]

# Try to load the require modules bail out if not found
$Modules=['uri','net/https','optparse']

# defualt program verbosity
$verbose = false

begin
    $Modules.each {|mod| require mod}
rescue LoadError
    puts "[!] Failed to load required modules, " + $!.message
    exit(1)
end

class OptparseSqid
    def self.parse(args)
      http_options = Hash.new
      sqid_options = Hash.new

      sqid_options['mode'] = nil
      sqid_options['start'] = 0
      sqid_options['nos'] = 20
      sqid_options['trigger'] = ["'"]
      http_options['timeout'] = 10
      http_options['proxy'] = nil
      http_options['proxy_auth'] = nil
      http_options['basic_auth'] = nil
      http_options['useragent'] = "SQID/#{$program[1]}"
      http_options['cookie'] = nil
      http_options['referer'] = nil
      sqid_options['dbfiles'] = ["sqid.db"]
      http_options['ac_cookies'] = false
      sqid_options['uwnq'] = false

      opts = OptionParser.new do |opts|
        opts.banner = "Usage: #{__FILE__} [options]"

        opts.separator ""
        opts.separator " options:"

        opts.on("-m", "--mode MODE",String,[:google,:url,:page,:crawl], "Operate in mode MODE.",
                                     "MODE is one of",
                                     "  g,google  Operate in google search mode.",
                                     "  u,url     Check this url or a file with urls.",
                                     "  p,page    Check single page.",
                                     "  c,crawl   Crawl website and check.")  do |mode|
           sqid_options['mode'] = mode
        end
        
        opts.separator ""
        opts.separator "Google search mode options:"

        opts.on("-q","--query QUERY",String,"QUERY to perforn google search for.") do |query|
               sqid_options['query'] = query
        end
        
        opts.on("-s","--start START",Integer,"zero-based index of the first desired result,",
                                           "zero if not specified.") do |start|
                sqid_options['start'] = start
        end
        
        opts.on("-r","--results RESULTS",Integer,"number of results desired, default is 20 if not specfied.","rounded to tens.") do |nos|
                  sqid_options['nos'] = nos
        end
        
        opts.separator ""
        opts.separator "URL check mode options:"
        
        opts.on("-u","--url URL",Array,"check this URL.","If URL is a file urls will be loaded from this file, specify each url on a new line.") do |url|
               if file_exists(url[0]) == true
                  sqid_options['urls']=[]
                  f=File.open(url[0],"r")
                  while line=f.gets
                      line.chomp!
                      sqid_options['urls'] << line if line =~ /^http[s]?:\/\//
                  end
                  f.close()
               else 
                 raise OptionParser::InvalidArgument,url[0] + ", not a valid url."  if !(url[0] =~ /^http[s]?:\/\//)
                 sqid_options['urls'] = url
               end
        end
        
        opts.separator ""
        opts.separator "Page check mode options:"
        
        opts.on("-p","--page PAGE","Check this page.") do |page|
               raise OptionParser::InvalidArgument,page + ", not a valid web page."  if !(page =~ /^http[s]?:\/\//)
               sqid_options['page'] = page
        end
        
        opts.separator ""
        opts.separator "Crawl mode options:"
        
        opts.on("-c","--crawl WEBSITE",String,"Crawl website WEBSITE and check.","specfify as http[s]://WESITE:[PORT], default PORT is 80") do |website|
            raise OptionParser::InvalidArgument,website + ", not a valid website."  if !(website =~ /^http[s]?:\/\//)
            sqid_options['website'] = website
        end
        
        opts.separator ""
        opts.separator "URL, Page and Crawl mode common options:"
        
        opts.on("-C","--cookie COOKIE",Array,"Cookie in the HTTP header specify as name=value,name=value.",
                                         "If COOKIE is a file cookies will be loaded from this file, specify each cookie on a new line.") do |cookie|
            raise OptionParser::AmbiguousOption, ", cookie option only valid in URL,PAGE or CRAWL mode of operation." if sqid_options['mode'] == :google 
               if file_exists(cookie[0]) == true
                  http_options['cookie'] = ""
                  f=File.open(cookie[0],"r")
                  while line=f.gets
                      line.chomp!
                      http_options['cookie'] += line+";"
                  end
                  f.close()
               else 
                  http_options['cookie'] = cookie.join(";")
               end
        end
        
        opts.on("-a","--accept-cookies","Accept cookies from the webite or page. Default is no.") do |ac_cookies|
               http_options['ac_cookies'] = ac_cookies
        end
        
        opts.on("-R","--referer REFERER",String,"Set referer in the HTTP header.") do |referer|
            raise OptionParser::AmbiguousOption,referer + ", referer only valid in URL,PAGE or CRAWL mode of operation." if sqid_options['mode'] == :google 
            http_options['referer'] = referer
        end
        
        opts.on("-B","--auth CREDENTIALS",String,"Use crendtials as basic auth for the website.","specfify as user:password.") do |basic_auth|
            raise OptionParser::AmbiguousOption,basic_auth + ", basic auth only valid in URL,PAGE or CRAWL mode of operation." if sqid_options['mode'] == :google 
            raise OptionParser::InvalidArgument,basic_auth if basic_auth.split(":").length != 2
            http_options['basic_auth'] = basic_auth
        end

        opts.separator ""
        opts.separator "Common options:"
        

        opts.on("-o", "--with-noquery", "Match page content without query parameters. Default is false.") do |uwnq|
            sqid_options['uwnq'] = uwnq
        end
        
        opts.on("-D","--db-files FILE,...,FILE",Array,"Use file(s) FILE,...,FILE as signature database.") do |dbfiles|
            dbfiles.each do |dbfile|
                raise OptionParser::InvalidArgument,dbfile + ", unable to load this file." if file_exists(dbfile) == false
            end
            sqid_options['dbfiles'] = dbfiles
        end

        opts.on("-t","--trigger TRIGGER",Array,"Use TRIGGER for detecting SQL injections/errors default is '.",
                                                "If TRIGGER is a file triggers will be loaded from it. specify each trigger on newline.",
                                                "Lines starting with a # are ignored." ) do |trigger|
               if file_exists(trigger[0]) == true
                  sqid_options['trigger'] = []
                  f=File.open(trigger[0],"r")
                  while line=f.gets
                      sqid_options['trigger'] <<  URI.escape(line.chomp!) if ! ( line =~ /^#/ )
                  end
                  f.close()
               else 
                  sqid_options['trigger'] = trigger
               end
        end
        
        opts.on("-T","--time-out TIMEOUT",Integer,"Timeout for response in seconds.","Default is 10 seconds.") do |timeout|
            http_options['timeout'] = timeout
        end
        
        opts.on("-U","--user-agent USERAGENT",String,"User Agent in the HTTP Header. Default is #{http_options['useragent']}.") do |useragent|
            http_options['useragent'] = useragent
        end
        
        
        opts.on("-P","--proxy PROXY",String,"User HTTP proxy PROXY for operations.","specfify as proxy:port.") do |proxy|
            raise OptionParser::InvalidArgument,proxy if proxy.split(":").length != 2
            http_options['proxy'] = proxy
        end
        
        opts.on("-A","--proxy-auth CREDENTIALS",String,"Use crendtials CRENDENTIALS for the proxy.","specfify as user:password.") do |proxy_auth|
            raise OptionParser::AmbiguousOption,proxy_auth + ", missing proxy with proxy credentials." if ! http_options['proxy']
            raise OptionParser::InvalidArgument,proxy_auth if proxy_auth.split(":").length != 2
            http_options['proxy_auth'] = proxy_auth
        end
        
        
        opts.on("-v", "--verbose", "Run verbosely.") do |verbose|
            $verbose = true
        end
        
        opts.on_tail("-h", "--help", "Show this message") do
          puts opts
          exit
        end

      end
      
      begin 
          opts.parse!(args)
          
          raise OptionParser::MissingArgument,"-m, no mode of operation." if ! sqid_options['mode']  
          
          case sqid_options['mode']
          
          when :google
              raise ArgumentError,": -q, query must be specified in GOOGLE mode."   if ! sqid_options['query']
          when :url
              raise ArgumentError,": -u, url must be specified in URL check mode."  if ! sqid_options['urls']
          when :page
              raise ArgumentError,": -p, page must be specfied in PAGE check mode." if ! sqid_options['page']
          when :crawl
              raise ArgumentError,": -c, website must be specfied in CRAWL mode."   if ! sqid_options['website']
          end  
      rescue SystemExit
          exit
      rescue Exception => e
          puts "[-] Error " +  e,"[*] #{__FILE__} -h for options."
          exit
      end
      [ http_options , sqid_options ]
    end  # parse()
    def self.file_exists(file)
        begin
            f=File.open(file,"r")
            f.close()
        rescue
            return false
        end
        true
    end # file_exists()
end  # class OptparseSqid

# class SqidHTTP
# Handles HTTP connection

class SqidHTTP
    @@HTTP=nil
    def initialize(url,http_opts) 
        @uri       = URI.parse(url)
        @address   = @uri.host
        @port      = @uri.port
        @timeout   = ( http_opts['timeout'] || 10 )
        @p_addr,@p_port = nil,nil
        @p_addr,@p_port = http_opts['proxy'].split(":") if http_opts['proxy']
        @p_user,@p_pass = nil,nil
        @p_user,@p_pass = http_opts['proxy_auth'].split(":") if http_opts['proxy_auth']
        @user,@password = http_opts['basic_auth'].split(":") if http_opts['basic_auth']
        @useragent = http_opts['useragent']
        @cookie    = http_opts['cookie']
        @referer   = referer
        @ac_cookie = ( http_opts['ac_cookies'] || false )
        @path      = @uri.path
        @path      = "/" if @uri.path == "" 
        @path      = (@uri.path + "?" + @uri.query) if @uri.query        
        @header= {
            "User-Agent" => @useragent
            }
        @header["Referer"]  = referer if @referer
        @header["Cookie"]  = cookie  if @cookie
        @@HTTP=Net::HTTP.new(@address,@port,@p_addr,@p_port,@p_user,@p_pass)
        @@HTTP.read_timeout=@timeout
        #@@HTTP.set_debug_output $stderr
        @@HTTP.use_ssl = true if @uri.scheme=="https"
   end
    
   def get
       begin
        url=@path
        request=Net::HTTP::Get.new(url,@header)
        request.basic_auth @user,@pass if @user and @password
        response=nil 
        response= @@HTTP.start { |http| http.request(request) }
        cookie=response['Set-Cookie']
        if @ac_cookie == true and cookie != nil
             @header['Cookie']=@cookie=cookie
        end
        puts "[*] Warning: Client error %d %s, %s." % [ response.code,response.message,@uri] if Integer(response.code) / 100 == 4
        response
       rescue Timeout::Error
           puts "Timed out => " + @uri.to_s
       rescue 
           puts "Error " + $!.message + ", %s." % @uri.to_s
       end
   end

   def useragent=(useragent)
       @header["User-Agent"]=@useragent=useragent
   end

   def cookie=(cookie)
       @header["Cookie"]=@cookie=cookie
   end

   def add_cookie(cookie)
       @cookie += ";" + cookie
       @header["Coookie"]=@cookie
   end
   
   def referer=(referer)
       @header["Referer"]=@referer=referer
   end
   attr_reader :address,:port,:p_addr,:p_user,:p_pass,:user,:password,:useragent,:cookie,:referer,:headers
   attr_writer :path,:user_agent,:user,:password,:cookie,:referer

end # class SqidHTTP 

# Sqid Core class

class Sqid
    def initialize(db_files)
	# This hash holds the errors and their regex
	@SQLErrors=Hash.new()
        db_files.each do |db_file|
            load_signatures(db_file)
        end
    end
    
    def load_signatures(db_file)
	begin
	    File.open(db_file,"r") do |file|
    		while line=file.gets
		    line=line.strip()
		    if line =~ /^#/ || line == ""
			next
		    end
		    a=line.split("|",2)
		    @SQLErrors.store( Regexp.new( a[0].strip() ) , a[1].strip() )
		end
	    end
            puts "[v] Loaded %d signatures from %s." % [@SQLErrors.size,db_file] if $verbose
	rescue Errno::ENOENT
	    puts "[!] Failed to load signatures, " + $!.message
	    exit(1)	
	rescue
	    puts "[!] Failed to load signatures, corrupted signatures file - #{db_file}."
	    exit(1)
	end
    end

    # Accepts a string and returns an array of matches
    def match(body)
        body.gsub!(/[\r,\n]?/,"")
        matches=[]
        @SQLErrors.each do |key,value|
            if body =~ /#{key}/
                matches << "#{value}"
            end
        end
        matches
    end
    attr_reader :SQLErrors
end

# class SqidURL check the url and report matches
class SqidURL < Sqid

    def initialize(http_opts,sqid_opts)
        @urls       = ( sqid_opts['urls'] || [] )
        @triggers   = sqid_opts['trigger']
        @http_opts  = http_opts
        # trach checked urls with this
        @curls = Hash.new()
        # track visited urls with this
        @vurls = Hash.new()
        @uwnq = sqid_opts['uwnq']
        @valid_pages =  [ "htm","html","shtml","xhtml","xml","php","asp","aspx","cfm","cfc","jsp","cgi","py","pl","rb","do"] 

        super(sqid_opts['dbfiles'])
    end

    def get(url)
        http_obj = SqidHTTP.new(url,@http_opts)
        http_res = http_obj.get
        return if http_res == nil
        http_res
    end
    
    def check
       puts "[*] Going to check %d urls." % (@urls.size)
       puts "\n"
       @urls.each do |url|
           self.check_url(url)
       end
       puts "\n[*] Checked %d URLs." % (@curls.size)
    end
    
    def check_url(url)    
       return if self.checked? url
       return if skipurl? url
       
       puts "[v] Checking URL %s.\n" % url if $verbose
       
       get_test_urls(url) { |test_url| 
           http_res = self.get(test_url)
           next if http_res == nil
           matches=match(http_res.body) if http_res.body
           matches.each do |match| 
                    puts "#{http_res.code} " + match + " => " + test_url
           end
           puts "#{http_res.code} No match => " + test_url if matches.empty? and http_res.code == "500"
       }
       self.checked url
    end
    
    # This gives us case urls for test for ex. if url is http://www.foo.com/foo?a=1&b=1 it gives
    #   http://www.foo.com/foo?a='&b=1
    #   http://www.foo.com/foo?a=1&b='
    
    def get_test_urls(url)
        obj = URI.parse(url)
        q = obj.query
        p = q.split("&") if q != nil
        if ( @uwnq == true ) and ( q == nil )
            yield url
            return
        end
        return if p == nil
        p.each do |parm|
            @triggers.each do |trigger|
                obj.query = q.gsub(Regexp.new(Regexp.quote(parm)),parm.gsub(/=.*/,"=#{trigger}"))
                yield obj.to_s 
            end
        end
    end
    
    def push_hash(hash,url)
        o = URI.parse(url)
        q = o.query
        o.query = nil
        bu = o.to_s
        if q == nil
            hash[bu]=[]
        else
            p=q.split("&")
            hash[bu]=[]
            p.each do |parm|
                parm.gsub!(/=.*/,"")
                hash[bu].push(parm)
            end
        end
     end

    def visited(url)
        self.push_hash(@vurls,url)
    end

    def checked(url)
        self.push_hash(@curls,url)
    end
    
    def exists?(hash,url)
        o = URI.parse(url)
        q = o.query
        o.query = nil
        bu = o.to_s
        return false if hash[bu] == nil
        if q 
            p=q.split("&")
            p.each do |parm|
                parm.gsub!(/=.*/,"")
                return true if hash[bu].index(parm) == nil
            end
        end
        true
    end

    def checked?(url)
        self.exists?(@curls,url)
    end

    def visited?(url)
        self.exists?(@vurls,url)
    end

    def do
        check
    end
    
    def skipurl?(url)
        validpath?(URI.parse(url).path) == false
    end

    def validpath?(path)
        @valid_pages.rindex(getext(getpage(path))) != nil
    end

    def hasext?(path)
        getext(getpage(path)) != nil
    end
    
    def getpage(path)
        a=path.split("/")
        a[a.length-1] 
    end

    def getext(page)
       page.downcase.split(".")[1] if page != nil
    end
    
    attr_writer :urls
end #class SqidURL

class SqidGOOGLE < SqidURL
    def initialize(http_opts,sqid_opts)
        @query = sqid_opts['query']
        @start = sqid_opts['start']
        @nos   = sqid_opts['nos']
        @http_opts = http_opts
        super(@http_opts,sqid_opts)
        search
    end

    def upto_in_10s(num)
	r=Array.new()
	while num > 0
            r.push(10)
            num=num-10
	end
	r.push(num) if num != 0
	return r
    end

    def search
        puts "[+] Getting %d links from search %s starting from %d." % [ @nos, @query, @start ]
        http_obj = SqidHTTP.new("http://www.google.com",@http_opts)
        upto_in_10s(@nos).each do |maxResults|
            search_str="/xhtml/search?mrestrict=xhtml&site=search&q=" + URI.escape(@query) + "&start=" + String(@start) + "&sa=N"
            http_obj.path = search_str
            http_res = http_obj.get
            return if http_res == nil
            http_res.body.gsub!(/[\r][\n]?/,"")
            http_res.body.scan(/href\s*=\s*\"*[^\">]*/) { |t|
                @urls.push(t.split("&amp;u=")[1])
            }
            @start+=maxResults
        end
        @urls.compact!()
        @urls.collect! {|url| URI.unescape(url)}
        puts "[+] Done got %d links." % @urls.size
    end
    def do
        check
    end
end

class SqidPAGE < SqidURL
    def initialize(http_opts,sqid_opts)
       @http_opts = http_opts
       @page      = sqid_opts['page']
       super(http_opts,sqid_opts)
    end
    
    def do
       puts "[+] Getting links from page  %s.\n" % @page
       get_links(@page) { |link| @urls.push(link) }
       puts "[+] Done got %d links." % @urls.size
       super
    end
    
    def get_links(url)
        return if url == nil
        a = SqidHTTP.new(url,@http_opts)
        r = a.get
        page =""
        page = r.body if r

        yield_url = URI.parse(url)
        base_path = URI.parse(url).path
        base_path = base_path[1...base_path.length] if base_path.length >= 1
        
        page.scan(/href\s*=\s*["']([^"']+)["']/i) { |link|
            link=URI.escape(link[0])
            begin
                u = URI.parse("#{link}")
                if u.scheme
                    next if !( u.scheme =~ /http[s]?:\/\//i )
                end
                if u.relative?
                    next if u.path == "/"
                    next if u.path.rindex("..")
                    if u.path[0] == "/"
                        yield_url.path = u.path
                        yield yield_url.to_s
                    end
                    t = base_path.split("/")
                    if hasext? base_path
                        if t.length > 1
                          t = t[0...t.length-1]
                       end
                    end
                    add_path=t.join("/")
                    yield_url.path = "/" + add_path + "/" + u.path

                    yield yield_url.to_s if not skipurl?(yield_url.to_s)
                else 
                    yield link if not skipurl?(link)
                end
            rescue 
                puts "[*] Invalid URL: " + $!.message
                next
            end
        }
    end
end

class SqidCRAWL < SqidPAGE
    def initialize(http_opts,sqid_opts)
        @website = sqid_opts['website']
        @host    = URI.parse(@website).host
        super(http_opts,sqid_opts)
    end
   
    def do
       puts "[+] Crawling %s.\n" % @website
       crawl(@website)
       puts "[+] Done got %d links." % @urls.size
       check
    end
    
    def crawl(url)
        puts "[v] Getting %s." % url if $verbose
        get_links(url) { |eurl| 
             eurl.gsub!(/#.*/,"")
             eurl_obj=URI.parse(eurl)
             if visited?(eurl) == false and eurl_obj.host == @host
                 visited eurl
                 @urls.push eurl
                 crawl(eurl)
             end
        }
    end
end

if $0 == __FILE__
    begin
        puts "#{$program.join(" v")} - SQL Injection digger.\n"
        puts "Copyright (C) Metaeye Security Group - http://sqid.rubyforge.org\n\n"
        x , y = OptparseSqid.parse(ARGV)
        a = Kernel.const_get("Sqid" + y['mode'].to_s.upcase).new x , y
        a.do
    rescue Interrupt
        puts "[!] Interrupted aborting."
    rescue
        puts "[-] Operation falied: " + $!.message
    end
end
