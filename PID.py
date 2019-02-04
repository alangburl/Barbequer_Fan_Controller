#Error calculation from PID controller
def calculate(desired,actual,DT,ui_past=0,error_past=0):
    '''calculate pid controller''' 
    ki=0.001
    kd=.01
    kp=.01                   
    uimax=10
    error= actual-desired
    up=error*kp
    ui=ki*error*DT+ui_past
    ui_past=ui
    
    if ui>uimax:
        ui=uimax
    elif ui<-uimax:
        ui=uimax
        
    ud=kd*(error-error_past)/DT
    error_past=error
    ut=up+ui+ud
    return ut,ui,error