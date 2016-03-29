---
layout: article
permalink: /posts/2015-12-15-harvesting-twitter-streams
title: "Harvesting the Twitter Streaming API to WARC files"
author: justin_littman 
excerpt: "The Twitter Streaming API is very powerful, allowing harvesting tweets not readily available from the other APIs."
---

The Twitter Streaming API is very powerful, allowing harvesting tweets not readily available from the other APIs. However, recall from our previous post that the Twitter Streaming API does not behave like REST APIs that are typical of social media platforms -- see Twitter’s description of the differences. A single HTTP response is potentially huge and may be collected over the course of hours, days, or weeks. This is a poor fit for both the normal web harvesting model in which a single HTTP response is recorded as a single WARC response record in a single WARC file, and for most web archiving tools, which store HTTP responses in-memory and don’t write them to the WARC file until the response is completed.

This post describes an approach we’ve developed for harvesting the Twitter Streaming API and recording in WARC files. We will also show how the tweets can be extracted from the WARC files for use by a researcher.

The Twitter Streaming API is not the only form of streaming content on the Web and the authors of WARC Specification had the forethought to support record segmentation. In record segmentation, a single HTTP response is split into multiple WARC records, potentially in multiple WARC files. The first record is a WARC response record; subsequent records are WARC continuation records. The header of the final continuation record also contains the total number of bytes of the entire HTTP response.

While WARC record segmentation is theoretically a good solution for the Twitter Streaming API, record segmentation is not widely supported in most web archiving tools. Our first step was to modify Internet Archive’s warcprox to support record segmentation. (Our pull request is #15. The crux of the change is between lines 210 and 245 in warcprox.py.) Recall from the earlier post that warcprox is an HTTP proxy that records the HTTP transaction in a WARC.

The following shows snippets from a WARC file created by the modified warcprox from the Twitter filter API retrieved by twarc tracking “obama”. It consists of a WARC response record, a request record, a continuation record, and a final continuation record.


WARC/1.0
WARC-Type: response
WARC-Record-ID: <urn:uuid:9aff4bf7-d64a-411c-9ef8-cd82778e036e>
WARC-Date: 2015-12-02T16:59:07Z
WARC-Target-URI: https://stream.twitter.com/1.1/statuses/filter.json
WARC-IP-Address: 199.16.156.20
Content-Type: application/http;msgtype=response
WARC-Segment-Number: 1
Content-Length: 1149
WARC-Block-Digest: sha1:7c8de1bd439cf62c67f9f4b0c48e6f3ae39eb4ef
WARC-Payload-Digest: sha1:cc1b7bf9a2945ddf8ae7c35d5f05513d0d8b691b

HTTP/1.1 200 OK
connection: close
content-Encoding: gzip
content-type: application/json
date: Wed, 02 Dec 2015 16:59:07 GMT
server: tsa
transfer-encoding: chunked
x-connection-hash: 8439cf557d0f807635797377d9e7d0b6

a
?
1f1
tSۊ?0??A/}?%??ر??^???¶??P?q#"KF??n??w?ٔ%?O3?͜?y`?GQ    Y?~?????!+?U??
^r? ?ي?bZ???r^WeU?_?:[?ѓ??$?"?I?7????1`?ہ?;?oH?}?a?v?.?ε
                                                        }???F???t??|???N??????m?i?t??9?
??1???B?c?A?<?;a?/???&?d?dkziR?Vxͽ????q                                                ??8?څ??;?Z
"?c'c?$g?????
????
    4???ʁ|???5?Y-k???z???9FM?<v{?v픗2K>_?2!??d????q?v???E?{|??ct???=???=n??_E
IQ?'?
U?&??]???n?ֽ??"?(:*?6,???F??????4:?%??
?=-??x?-ל????EQ????N>?????VOW???c'\???^gk?Z=???lZ???y??
163
?U?n?0???C?^??Æ^
=?T?)?4X_U????7~T?75??~Q?˵Ғ1??????`"????c?wfgR?`?g???kp<???r)+.
?4zD?????ie6?/F????˭*???   Xm??rLhEiƈs???B)y???b;a??Am??d׮?<??ԍNȄ?$????T?r?ϝ,ot?m???L???
                        ?j4??.??Q??b???%????7?????????7??XT?2B%?,aQ?4I?p??wn?z
                                                                                ??\??7`
                                                                                       R{Z???8?Ϲ<?$?t??)u?^?5?u?{}?K??yOo?]?(??.f??|??m????
229
[o?0???'q???6??-J?.?z@k'??IL@??

WARC/1.0
WARC-Type: request
WARC-Record-ID: <urn:uuid:3a6ce873-13a9-401a-bfd9-3ddc321aab96>
WARC-Date: 2015-12-02T16:59:07Z
WARC-Target-URI: https://stream.twitter.com/1.1/statuses/filter.json
WARC-Concurrent-To: <urn:uuid:9aff4bf7-d64a-411c-9ef8-cd82778e036e>
WARC-Block-Digest: sha1:fa301cb54fd6c38adac4a43bacf36d38198ec8e0
Content-Type: application/http;msgtype=request
Content-Length: 566

POST /1.1/statuses/filter.json HTTP/1.1
content-length: 30
accept-encoding: deflate, gzip
host: stream.twitter.com
accept: */*
user-agent: python-requests/2.8.1
content-type: application/x-www-form-urlencoded
authorization: OAuth oauth_nonce="149931870481283598461449075546", oauth_timestamp="1449075546", oauth_version="1.0", oauth_signature_method="HMAC-SHA1", oauth_consumer_key="EHdoTe7ksBgflP5nUalEfhaeo", oauth_token="481186914-c2yZjbk1np0Z5MWEFYYQKSQNFBXd8T9r4k90YkJl", oauth_signature="m0hHjrPnU7aTtOhjmk8om3Vv7Ok%3D"

track=obama&stall_warning=True

WARC/1.0
WARC-Type: continuation
WARC-Record-ID: <urn:uuid:c18791da-24e0-42a7-91df-82dfdae6697e>
WARC-Date: 2015-12-02T16:59:07Z
WARC-Target-URI: https://stream.twitter.com/1.1/statuses/filter.json
WARC-IP-Address: 199.16.156.20
Content-Type: application/http;msgtype=response
WARC-Segment-Number: 2
WARC-Segment-Origin-ID: <urn:uuid:9aff4bf7-d64a-411c-9ef8-cd82778e036e>
Content-Length: 1220
WARC-Block-Digest: sha1:82794503724ba3bb06fee69302614a3f5ef00c39

?????a??N?*M???_l???y"uU]IZ`RU1?/?n?V?`???&H??h?U??x??Ea j???mٌSjfsr¨??ê˽RN?&F'?<?h^H~ ?è?ـ
                                                                                            ??m?@?'?]???:?sT?T?/S??W??t??]M???_??.???o?ҷa??Sn1???/?;Z;?+?PF??
                                       $L?HnD?????x?t?|ľ?    ?    -G^?|?    "?????gr?? ? )?e[????{]vW???j???-??*T&?{)2\?9^?`\?_??>?.-????ҚO??{v?+?W??4??ps %c?8?'?`?nU???a??%?q?/q?о?X???&???G}71G?&V?
                                                                                  ?w?ȱZn?ӯ?&?*C??&s?R???rRa???? ?j??es??q?@?s??\/7?w??v?????+???2(????????mNS?
?iZ?????p}?8?.?????????;??
16c
̘AO?0ǿ
     g?F˸??&?!?u???2D????&U?Ń'J?ڒ??????????K5??pBm?T??=)?0?
                                                           8Ę?????Ԉ,?
                                                                     O??>u?~???3?A???Ώho??[?rYV'??jW??J?e?IV?r?d?*L6    ;???????i/
R-       ??
  ??Y?Cĭ??
          ??2]vj ??7??C5B??????!?;????m(j???^?d/??jK??m?d?K ,???|P˂?ۥF2??5*%`Lﲞ?x\g????'qs?F?
                                                                                               ?O?
                                                                                                  ?=Ԥz`??k+?l?gS????
                                                                                                                    qU?g#?S????3??SӕS???`2=HM?-?
??Ys?5S?O???
68
??    U??X?<???̀4?B???Q'Ԇ7(?!?S?፮?>F??^??????Rm,?A????r?<(e??:?28;?f????
1a1
??OO?@??&~    ?"?"??D?5?Lj6P?,?@K??    [
?F?`????~? ???<?T5? ???%'ap,$?FCZ????vP???D?N?8p?-/???l[??y???#?{]??(?J????'E?&΃???զj???X??7?<Ɩg?ՅU?Bh%
                                                                                                           m??u?h????????s?N??u????u??0֜d

WARC/1.0
WARC-Type: continuation
WARC-Record-ID: <urn:uuid:d7bfe010-7831-45a8-8361-715692ea014b>
WARC-Date: 2015-12-02T16:59:09Z
WARC-Target-URI: https://stream.twitter.com/1.1/statuses/filter.json
WARC-IP-Address: 199.16.156.20
Content-Type: application/http;msgtype=response
WARC-Segment-Number: 3
WARC-Segment-Origin-ID: <urn:uuid:9aff4bf7-d64a-411c-9ef8-cd82778e036e>
WARC-Segment-Total-Length: 924
WARC-Truncated: unspecified
Content-Length: 307
WARC-Block-Digest: sha1:57b73cdaab8025cc04a83f3ae6eff2dd6e2bfa15

?^,~0??Cc?43??n????8???????A^]d???ן&??qSN?FZ
??m?$p? ?&?A?p$?$?S??d,^zk?#?Y    ?q?g~????R????P?\???~??w??T?&`
                                                              ????L?r????i????Th2?2B??$?C??:????T?????
20e
tRMk?@?+??C]YV??T
NqZHS?K/??F???Y?QE?|GVjB?u?a?y??͋(,J??Vz???X?

??̲i??)|???$?L?H?Rd?y???"

As should be obvious, this data is not readily usable by most researchers. In particular, there are four barriers to use:

It is in a WARC file.
The HTTP response is segmented into multiple WARC records.
The HTTP response has gzip content encoding.
The HTTP response has chunked transfer encoding.
In order to be confident in this approach, we feel it is prudent to make sure that we can access the tweets given these various barriers and the lack of support for record segmentation in web archiving tools. To this end, we developed TwitterStreamWarcIter and the parent class BaseWarcIter.  TwitterStreamWarcIter outputs the tweets from a WARC file, one per line. This is the same output as twarc or cat-ing a line-oriented json file and can be piped to other tools such as jq:


$ python twitter_stream_warc_iter.py test_1-20151202200525007-00000-30033-GLSS-F0G5RP-8000.warc.gz

{"contributors": null, "truncated": false, "text": "RT @Litorodbujan: Obama quiere visitar Espa\u00f1a!\nAhora s\u00ed somo
s un pa\u00eds serio; con Rajoy no se repetir\u00e1 esto.   #RajoyconPiqueras https://t.c\u2026", "is_quote_status": false,
 "in_reply_to_status_id": null, "id": 672144412936445952, "favorite_count": 0, "source": "<a href=\"https://mobile.twitter.
com\" rel=\"nofollow\">Mobile Web (M2)</a>", "retweeted": false, "coordinates": null, "timestamp_ms": "1449086690540", "ent
ities": {"user_mentions": [{"id": 320317854, "indices": [3, 16], "id_str": "320317854", "screen_name": "Litorodbujan", "nam
....

or suitable for human-consumption with the --pretty flag:


$ python twitter_stream_warc_iter.py test_1-20151202200525007-00000-30033-GLSS-F0G5RP-8000.warc.gz --pretty

{
    "contributors": null, 
    "truncated": false, 
    "text": "RT @Litorodbujan: Obama quiere visitar Espa\u00f1a!\nAhora s\u00ed somos un pa\u00eds serio; con Rajoy no se repetir\u00e1 esto.   #RajoyconPiqueras https://t.c\u2026", 
    "is_quote_status": false, 
    "in_reply_to_status_id": null, 
    "id": 672144412936445952, 
    "favorite_count": 0, 
    "source": "<a href=\"https://mobile.twitter.com\" rel=\"nofollow\">Mobile Web (M2)</a>", 
    "retweeted": false, 
    "coordinates": null, 
    "timestamp_ms": "1449086690540", 
    "entities": {
....

This approach addresses the WARC barrier by using Internet Archive’s WARC library to read the WARC file. The IA WARC library is extended to handle record segmentation by stitching the payload back together. (See CompositeFilePart. It still doesn’t handle continuations that are in other WARC files, but solving that problem is just software development.) And lastly, the content encoding and transfer encoding barriers are remedied by loading the payload into a urllib3 HTTPResponse which handles the decoding of the content encoding and transfer encoding, as well as providing a familiar, pythonic interface to the response.

As we have explored the similarity between web harvesting and social media harvesting, the Twitter Streaming API represents the point of greatest friction. However, the above represents a reasonable first approach to addressing the unique features of the Twitter Streaming API.

(This post originally appeared on the [Scholarly Technology Group's blog](https://library.gwu.edu/scholarly-technology-group/posts/harvesting-twitter-streaming-api-warc-files))
n the GW Libraries website.)
