#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:58:05 2022

@author: markusvonheim
"""

from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date
import numpy as np


def d1(S,K,T,r,sigma):
    return(log(S/K)+(r+sigma**2/2.)*T)/(sigma*sqrt(T))
def d2(S,K,T,r,sigma):
    return d1(S,K,T,r,sigma)-sigma*sqrt(T)

def bs_call(S,K,T,r,sigma,d):
    d1 = (log(S/K)+(r+sigma**2/2)*T)/(sigma*sqrt(T))
    d2 = d1 - sigma*sqrt(T)   
    Ct = S*norm.cdf(d1)-K*exp(-r*T)*norm.cdf(d2)                              
    delta_c = exp(-d*T)*norm.cdf(d1)
    gamma_c = exp(-d*T)*norm.cdf(d1)/(S*sigma*sqrt(T))
    theta_c = d*S*exp(-d*T)*norm.cdf(d1)-r*K*exp(-r*T)*norm.cdf(d2)-(K*exp(-r*T)*norm.cdf(d2)*sigma)/(2*sqrt(T))
    vega_c = (S*exp(-d*T)*norm.cdf(d1)*sqrt(T))/100                                  
    return Ct, delta_c, gamma_c, theta_c, vega_c
  

print(bs_call(40, 45, 91/365, 0.08, 0.3, 0))

# def bs_put(S,K,T,r,sigma):
    
    
#     return K*exp(-r*T)-S+bs_call(S,K,T,r,sigma)




# black_scholes_p <-  function(S, K, sigma, r, T, delta){
#   d1 = d1_f(S,K,r,delta,sigma,T)
#   d2 = d2_f(d1,sigma,T)
  
#   P_t = K*exp(-r*T)*pnorm(-d2)-S*exp(-delta*T)*pnorm(-d1)
#   delta_p = -exp(-delta*T)*pnorm(-d1)
#   gamma_p = exp(-delta*T)*dnorm(d1)/(S*sigma*sqrt(T))
#   theta_p = delta*S*exp(-delta*T)*pnorm(d1)-r*K*exp(-r*T)*pnorm(d2)-(K*exp(-r*T)*dnorm(d2)*sigma)/(2*sqrt(T))+r*K*exp(-r*T)-delta*S*exp(-delta*T)
#   vega_p = (S*exp(-delta*T)*dnorm(d1)*sqrt(T))/100
#   list = c(P_t, delta_p, gamma_p,theta_p, vega_p)
#   return(list)


