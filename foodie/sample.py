import requests


def web_scrapping(h_name):
    res = requests.get("https://restaurant-guru.in/"+h_name+"/reviews/google").text
    res_rating=res.split('<div class="fill ag_sel"')[1].split(">")[0].split(": ")[1].split("%")[0]
    print(res_rating)
    rating=(int(res_rating)*5)/100


    print(rating)



    res_comments=res.split('<div id="comments_container"')[1].split("data-id=")

    reviews=[]

    for i in range(1,len(res_comments)):
        try:
            r=res_comments[i]
            name=r.split('class="user_info__name"')[1].split('>')[1].split("<")[0]
            print(name)
            rating=int(r.split('style="width: ')[1].split('%;')[0])*5/100
            print(rating)
            review=r.split('class="text_full">')[1].split("<")[0]
            print(review)
            print("======================")
            row={"name":name,"rating":rating,"review":review}
            reviews.append(row)
        except:
            pass
    res1=requests.get("https://restaurant-guru.in/"+h_name).text
    # print(res1)
    imgs_res=res1.split('class="swiper-wrapper')[1]


    imgs_res=imgs_res.split('<img width="')
    images=[]
    for i in range(1,len(imgs_res)):
        img=imgs_res[i]
        img=img.split('src="')[1].split('"')[0]
        print(img)
        if "jpg" in img or 'png' in img or "jpeg" in img:
            images.append({"img":img})
    return rating,reviews,images