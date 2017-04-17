from picamera import PiCamera
from time import sleep



camera = PiCamera()
camera.rotation = 180
camera.start_preview(alpha=200)
frame = 1

context = { 'camera' : camera
            , 'frame' : frame
            , 'target_directory': '/home/pi/Desktop/stopmotion'
            , 'filename_format' : 'image%04d'
            , 'filename_ext' : 'jpg'
            , 'preview' : False
            , 'image_effects' : list(camera.IMAGE_EFFECTS.keys())
            , 'exposure_modes' : list(camera.EXPOSURE_MODES.keys())
            , 'awb_modes' : list(camera.AWB_MODES.keys())
            , 'drc_strengths' : list(camera.DRC_STRENGTHS.keys())
            , 'rotations' : [ 0 , 90, 180, 270 ]
            , 'isos' : [ 0, 100, 200, 320, 400, 500, 640, 800, 1600] 
            }

def initialize(ctx):
    pass
        

def capture(ctx):
    cam = ctx['camera']
    filename = str.format('{}/{}.{}', ctx['target_directory'], ctx['filename_format'] % ctx['frame'], ctx['filename_ext'])
    cam.capture(filename)
    print('capture : %s' % filename)
    ctx['frame'] += 1
    pass

def info(ctx):
    cam = ctx['camera']
    images_effects = cam.IMAGE_EFFECTS
    for fx in images_effects:
        print(fx)
    pass

def getNext(item, li):
    for idx, elem in enumerate(li):
        if elem == item:
            return li[(idx + 1) % len(li)]

def getPrev(item, li):
    for idx, elem in enumerate(li):
        if elem == item:
            return li[(idx - 1) % len(li)]

def image_effect(ctx,itr):
    cam = ctx['camera']
    if itr == '+':
        cam.image_effect = getNext(cam.image_effect,ctx['image_effects']) 
        pass
    if itr == '-':
        cam.image_effect = getPrev(cam.image_effect,ctx['image_effects'])
        pass
    print('image effect :', cam.image_effect) 
    pass

def drc_strength(ctx,itr):
    cam = ctx['camera']
    if itr == '+':
        cam.drc_strength = getNext(cam.drc_strength,ctx['drc_strengths']) 
        pass
    if itr == '-':
        cam.drc_strength = getPrev(cam.drc_strength,ctx['drc_strengths']) 
        pass
    print('drc strength :', cam.drc_strength) 
    pass

def exposure_mode(ctx,itr):
    cam = ctx['camera']
    if itr == '+':
        cam.exposure_mode = getNext(cam.exposure_mode,ctx['exposure_modes']) 
        pass
    if itr == '-':
        cam.exposure_mode = getPrev(cam.exposure_mode,ctx['exposure_modes']) 
        pass
    print('exposure mode :',cam.exposure_mode )
    pass

def awb_mode(ctx,itr):
    cam = ctx['camera']
    if itr == '+':
        cam.awb_mode = getNext(cam.awb_mode,ctx['awb_modes']) 
        pass
    if itr == '-':
        cam.awb_mode = getPrev(cam.awb_mode,ctx['awb_modes']) 
        pass
    print('AWB mode :',cam.awb_mode )
    pass
    
def isos(ctx):
    '''
    FIXME : no effect on preview : is it Normal ??
    '''
    cam = ctx['camera']
    ctx['camera'].iso = getNext(cam.iso, ctx['isos'])
    print('isos :', ctx['camera'].iso)
    pass

def alpha(ctx, amount):
    cam = ctx['camera']
    if cam.preview.alpha + amount > 255:
        cam.preview.alpha = 255
    else:
        if cam.preview.alpha + amount <= 0:
            cam.preview.alpha = 0
        else: 
            cam.preview.alpha = cam.preview.alpha + amount
    print('alpha : ', cam.preview.alpha)
    pass

def process_commande(commande, ctx):
    if len(commande) == 0:
        capture(ctx)
        return
    else:
        if commande.upper() == 'I':
            isos(ctx)
            return

        # controlling drc strength        
        if commande == 'D':
            drc_strength(ctx, '+')
            return
        if commande == 'd':
            drc_strength(ctx, '-')
            return

        # controlling image effects        
        if commande == 'F':
            image_effect(ctx, '+')
            return
        if commande == 'f':
            image_effect(ctx, '-')
            return

        # controlling exposure mode      
        if commande == 'X':
            exposure_mode(ctx, '+')
            return
        if commande == 'x':
            exposure_mode(ctx, '-')
            return

        # controlling exposure mode      
        if commande == 'W':
            awb_mode(ctx, '+')
            return
        if commande == 'w':
            awb_mode(ctx, '-')
            return
        
        # controlling PREVIEW ALPHA ( range [0..255] )
        if commande == '++':
            alpha(ctx, +255)
            return
        if commande == '--':
            alpha(ctx, -255)
            return            
        if commande == '+':
            alpha(ctx, +20)
            return
        if commande == '-':
            alpha(ctx, -20)
            return
# controlling PREVIEW ALPHA 
        
    pass

initialize(context)
while True:
    try:
        cmd = input('?>')
        process_commande(cmd, context)
#        photo = '/home/pi/Desktop/stopmotion/image%04d.jpg' % frame
#        camera.capture(photo)
#        print(photo)
#        frame += 1
    except (KeyboardInterrupt, SystemExit):
        
        camera.stop_preview()
        print('terminé')
        break
