import numpy as np
def agc(DataO: np.ndarray, time: np.ndarray, agc_type = 'inst',  time_gate = 500e-3):
    """
    agc: applies automatic gain control for a given dataset.

     Usage:
         gained_data = agc(data,time,agc_type, time_gate)

     Parameters
     -----------
     data: np.ndarray
            Input seismic data
     time: np.ndarray
            Time array
     agc_type: string <class 'str'>
            Type of agc to be applied. Options: 1)'inst': instantanous AGC. 2) 'rms': root-mean-square.
            For details, please refere to: https://wiki.seg.org/wiki/Gain_applications
     time_gate: float <class 'float'>
            Time gate used for agc in sec. Defualt value 500e-3.

     Returns
     -------
     gained_data: np.ndarray
        Data after applying AGC

        AGC is python function written by Musab Al Hasani based on the book of Oz Yilmaz (https://wiki.seg.org/wiki/Gain_applications)

    """
    data = np.copy(DataO)

    # # calculate nth-percentile
    # nth_percentile = np.abs(np.percentile(data, 99))

    # clip data to the value of nth-percentile
    # data = np.clip(data, a_min=-nth_percentile, a_max = nth_percentile)


    num_traces = data.shape[1] # number of traces to apply gain on
    gain_data  = np.zeros(data.shape) # initialise the gained data 2D array

    # check what type of agc to use
    if agc_type == 'rms':
        for itrc in range(num_traces):
            gain_data[:, itrc] = rms_agc(data[:, itrc], time, time_gate)

    elif agc_type =='inst':
        for itrc in range(num_traces):
            gain_data[:, itrc] = inst_agc(data[:, itrc], time, time_gate)

    else:
        print('Wrong agc type!')

    return gain_data



def rms_agc(trace: np.ndarray, time: np.ndarray,  time_gate=200e-3)-> np.ndarray:
    """

    rms_agc: apply root-mean-square automatic gain control for a given trace.

     Usage:
         gained_trace = agc(data,time,agc_type, time_gate)

     Parameters
     -----------
     data: np.ndarray
            Input seismic trace
     time: np.ndarray
            Time array
     time_gate: float <class 'float'>
            Time gate used for agc in sec. Defualt value 200e-3 here, though there is  not a typecal value to be used.

     Returns
     -------
     gained_trace: np.ndarray
        trace after applying RMS AGC

        RMS_AGC is python function written by Musab Al Hasani based on the book of Oz Yilmaz (https://wiki.seg.org/wiki/Gain_applications)

    """

    # determine time sampling and num of samples
    dt = time[1]-time[0]
    N = len(trace)

    # determine number of time gates to use
    gates_num = int((time[-1]//time_gate)+1)

    # initialise indecies for the coners of the gate
    time_gate_1st_ind = 0
    time_gate_2nd_ind = int(time_gate/dt)


    # construct lists for begining and ends of tome gates
    start_gate_inds = [(time_gate_1st_ind + i*time_gate_2nd_ind) for i in range(gates_num)]
    end_gate_inds = [start_gate_inds[j] + time_gate_2nd_ind  for j in range(gates_num)]

    # set last gate to the end sample
    end_gate_inds[-1] = N

    # initialise middle gate time and gain function arrays
    t_rms_values   = np.zeros(gates_num+2)
    amp_rms_values = np.zeros(gates_num+2)

    # loop over every gate
    ivalue = 1
    for istart, iend in zip(start_gate_inds, end_gate_inds):
        t_rms_values[ivalue]    = 0.5*(istart + iend)
        amp_rms_values[ivalue] = np.sqrt(np.mean(np.square(trace[istart:iend])))
        ivalue += 1

    # set side values for interpolation
    t_rms_values[-1] = N
    amp_rms_values[0] = amp_rms_values[1]
    amp_rms_values[-1] = amp_rms_values[-2]

    # linear interpolation for the rms amp function for every sample N
    rms_func = np.interp(range(N), t_rms_values, amp_rms_values )

    # calculate the gained trace
    gained_trace = trace*(np.sqrt(np.mean(np.square(trace)))/rms_func)


    return gained_trace


def inst_agc(trace, time, time_gate = 500e-3 ):
    """

    rms_agc: apply instantanous automatic gain control for a given trace.

     Usage:
         gained_trace = agc(data,time,agc_type, time_gate)

     Parameters
     -----------
     data: np.ndarray
            Input seismic trace
     time: np.ndarray
            Time array
     time_gate: float <class 'float'>
            Time gate used for agc in sec. typecal values between 200-500ms.

     Returns
     -------
     gained_trace: np.ndarray
        trace after applying instansous AGC

        INST_AGC is python function written by Musab Al Hasani based on the book of Oz Yilmaz (https://wiki.seg.org/wiki/Gain_applications)

    """
    # determine time sampling and num of samples
    dt = time[1]-time[0]
    N = len(trace)

    # determine the number of sample of a given gate
    end_samples = int(time_gate/dt)

    # calculate gates number not including the last end_samples
    gates_num = N - end_samples

    # initialise gates begining and end indices
    time_gate_1st_ind = 0
    time_gate_2nd_ind = int(time_gate/dt)

    # construct lists for indices of gates corners
    start_gate_inds = [i for i in range(gates_num)]
    end_gate_inds = [start_gate_inds[j] + time_gate_2nd_ind  for j in range(gates_num)]

    #initialise gain function
    amp_inst_values = np.zeros(N)

    # loop over ever sample to calculate gain function
    ivalue = 0
    for istart, iend in zip(start_gate_inds, end_gate_inds):
        amp_inst_values[ivalue] = np.mean(np.abs(trace[istart:iend]))
        ivalue += 1
    amp_inst_values[-end_samples:] = (amp_inst_values[ivalue-1])

    # calculate gained trace
    gained_trace = trace*(np.sqrt(np.mean(np.square(trace)))/amp_inst_values)

    return gained_trace
