from text2vec import Similarity

# Two lists of sentences

# sentences1 = ['如何更换花呗绑定银行卡',
#               'The cat sits outside',
#               'A man is playing guitar',
#               'The new movie is awesome']

# sentences2 = ['花呗更改绑定银行卡',
#               'The dog plays in the garden',
#               'A woman watches TV',
#               'The new movie is so great']

# sentences1 = ['派蒙,总算解决了.这么说来。之前在莎兰树的梦境里。也能看见这棵很神奇,的树呢!,[0106648797']

sentences1 = ['派蒙,总算解决了.这么说来。之前在莎兰树的梦境里。也能看见这棵很神奇,的树呢!,[0106648797']
# sentences1 = ['尝罗摩,晁数黑色的虫子在侵蚀梦之树在沙恒中的根。就算在梦申。也能感受到,无留']
sentences2 = ['訾罗摩,晁数黑色的虫子在侵蚀梦之树在沙恒中的根。就算在梦中,也能感受到,无留陀的手;在摇晃着这介梦。']

# Compute embedding for both lists
sim_model = Similarity()

for i in range(len(sentences1)):
    for j in range(len(sentences2)):
        score = sim_model.get_score(sentences1[i], sentences2[j])
        print("{} \t\t {} \t\t Score: {:.4f}".format(sentences1[i], sentences2[j], score))