# Basic example showing how to get a dataset
import handshape_datasets as hd


DATASET_NAME = "PugeaultASL_A"
#ersion=dict({'1':'WithGabor'})

#ciarp_info = hd.info(DATASET_NAME)
#x,metadata = hd.load(DATASET_NAME,version='WithGabor') ciarp
#x,metadata = hd.load(DATASET_NAME, version='bw') nus1
#x,metadata = hd.load(DATASET_NAME, version='hn')
x,metadata = hd.load(DATASET_NAME)
print(x.shape)
print(x[1])
print(x.max())
print(x.min())
for k in metadata:
    print(k,metadata[k].shape, metadata[k].min(), metadata[k].max())







#print(ciarp_info.summary())

#ciarp[0].show_dataset() #nunca devuelve un dataset, sino que en el caso de lsa16 devuelve un np.array y un dict (x y metadata)

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=128)

# ciarp.show_dataset(subsets=["test_Kinect_WithGabor"],samples=[1,2,3,0,15,1,200])
