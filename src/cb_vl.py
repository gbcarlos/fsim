

h = 0.01
g = 9.81

Az = -g     #g
Vz = 0.0    #V evtl zu berechnen
Pz = 100.0  #self.pos[1]
Ax = 0.0    #Nicht vorhanden
Vx = 500.0  #v0*cos(alpha) constant da keine reibung
Px = 0.0    #self.pos[0]
t = 0.0     #self.sim_time

def integrate(y, x):
    y = y + x * h
    return y

while True:
    print("%2.2f %8.2f %8.2f %8.2f %8.2f\n" % (t, Vz, Pz, Vx, Px))
    t = t+h
    Vz = integrate(Vz, Az)
    Pz = integrate(Pz, Vz)
    Vx = integrate(Vx, Ax)
    Px = integrate(Px, Vx)

    if Pz < 0:
        break