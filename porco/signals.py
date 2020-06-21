from blinker import Namespace

porco = Namespace()

booting = porco.signal("BOOTING")
after_boot = porco.signal("AFTER-BOOT")