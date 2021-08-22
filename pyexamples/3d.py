
import sys
sys.path.append('../')
from pycore.tikzeng import *
from pycore.blocks  import *

arch = [ 
    to_head('..'), 
    to_cor(),
    to_begin(),
    
    #input
    to_input( '../../t1.png', to='(-4.5,0,0)', name="t1"),
    to_input( '../../t1ce.png', to='(-4.0,0,0)', name="t1ce"),
    to_input( '../../t2.png', to='(-3.5,0,0)', name="t2"),
    to_input( '../../seg.png', to='(-3.0,0,0)', name="flair-east"),
    
    *block_2ConvPool("b1", "", "pool_b1", s_filer="(60$\\times$60$\\times$40)", n_filer=32, offset="(1,0,0)", size=(40,40,2), opacity=0.5),
    
    *block_2ConvPool("b2", "pool_b1", "pool_b2", s_filer="(30$\\times$30$\\times$20)", n_filer=64, offset="(2.5,0,0)", size=(20,20,4), opacity=0.5),
    *block_2ConvPool("b3", "pool_b2", "pool_b3", s_filer="(15$\\times$15$\\times$10)", n_filer=128, offset="(2,0,0)", size=(10,10,8), opacity=0.5),
    *block_2ConvPool("b4", "pool_b3", "ccr_res_b6", s_filer="(15$\\times$15$\\times$10)", n_filer=256, offset="(1,0,0)", size=(5,5,16), opacity=0.5),
    
    #Decoder
    *block_Unconv( name="b6", botton="ccr_b4", top='end_b6', s_filer="(30$\\times$30$\\times$20)",  n_filer=128, offset="(1,0,0)", size=(10,10,8), opacity=0.5 ),
    to_skip( of='ccr_b3', to='ccr_res_b6', pos=1.25),
    *block_Unconv( name="b7", botton="end_b6", top='end_b7', s_filer="(60$\\times$60$\\times$40)", n_filer=64, offset="(2,0,0)", size=(20,20,4), opacity=0.5 ),
    to_skip( of='ccr_b2', to='ccr_res_b7', pos=1.25),
    *block_Unconv( name="b8", botton="end_b7", top='end_b8', s_filer="(120$\\times$120$\\times$80)", n_filer=32, offset="(2.5,0,0)", size=(40,40,2), opacity=0.5 ),
    to_skip( of='ccr_b1', to='ccr_res_b8', pos=1.25),
    to_Conv( "end_conv", offset="(2.5,0,0)", to="(end_b8-east)", s_filer="", n_filer=1, width=2, height=40, depth=40),
    to_connection(
        "end_b8",
        "end_conv",
    ),
    #to_output( '../../seg.png', to='end_conv', xshift=2.5),
    to_end()
    ]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex' )

if __name__ == '__main__':
    main()
    
