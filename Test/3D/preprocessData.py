import numpy as np


def piA(x,mask,nrow,ncol,nSlice):
    """ This is a the A operator as defined in the paper"""
    ccImg=np.reshape(x,(nrow,ncol,nSlice) )
    kspace=np.fft.fftn(ccImg)/np.sqrt(nrow * ncol*nSlice)
    res=kspace[mask!=0]
    return res


def piAt(kspaceUnder,mask,nrow,ncol,nSlice):
    """ This is a the A^T operator as defined in the paper"""
    temp=np.zeros((nrow,ncol,nSlice),dtype=np.complex64)
    if len(mask.shape)==2:
        mask=np.tile(mask,(1,1))

    temp[mask!=0]=kspaceUnder
    img=np.fft.ifftn(temp)*np.sqrt(nrow * ncol*nSlice)
    #coilComb=np.sum(img*np.conj(csm),axis=0).astype(np.complex64)
    #coilComb=coilComb.ravel();
    return img.astype(np.complex64)

def generateUndersampled(org,mask,sigma=0.):
    nrow,ncol,nSlice = org.shape
    A  = lambda z: piA(z,mask,nrow,ncol,nSlice)
    At = lambda z: piAt(z,mask,nrow,ncol,nSlice)

    sidx=np.where(mask.ravel()!=0)[0]
    nSIDX=len(sidx)
    noise=np.random.randn(nSIDX,)+1j*np.random.randn(nSIDX,)
    noise=noise*(sigma/np.sqrt(2.))
    y=A(org) + noise
    atb=At(y)
    return atb
def cropdata(inp,patch_size):
    nrow,ncol,nSlice = inp.shape
    x = np.random.randint(nrow-patch_size[0]+1)
    y = np.random.randint(ncol-patch_size[1]+1)
    z = np.random.randint(nSlice-patch_size[2]+1)

    return inp[x:x+patch_size[0],y:y+patch_size[1],z:z+patch_size[2]]