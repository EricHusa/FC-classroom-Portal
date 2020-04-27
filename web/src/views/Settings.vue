<template>
  <div>
    <NavBar />
    <div class="center">
      <b-form @submit="onSubmit" inline align-center>
        <label>System: </label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          :value="currentDevice"
          v-model="currentDevice"
          :options="formatDevices"
          id="inline-form-input-system"
          style="margin-left: 1rem;"
        ></b-form-select>
        <b-button type="submit" variant="primary">Set</b-button>
      </b-form>
    </div>

    <div>
      <b-row>
        <b-col sm="4">
          <b-table
            ref="settingsTable"
            selectable
            select-mode="single"
            :items="options"
            :fields="headers"
            @row-selected="onRowSelected"
            responsive="sm"
          ></b-table>
        </b-col>

        <b-col sm="8">
          <b-jumbotron>
            <b-alert
              :show="updateAlert"
              dismissible
              fade
              variant="success"
              @dismissed="resetAlert"
            >
              {{ updateMessage }}
            </b-alert>
            <h2>{{ sectionTitle }} Settings</h2>
            <hr />

            <b-container fluid>
              <b-collapse
                :visible="sectionTitle === 'Account'"
                id="account-settings-collapse"
              >
                <b-form inline @submit="updateAccount">
                  <b-form-group
                    v-for="item in teacherOptions"
                    :key="item.key"
                    :description="item.label"
                  >
                    <b-input
                      :id="`account-input-${item.key}`"
                      v-model="teacherForm[item.key]"
                      :placeholder="teacherForm[item.key]"
                      style="margin: 0.5rem;"
                      required
                    ></b-input>
                  </b-form-group>
                  <b-button type="submit" variant="primary">Update</b-button>
                  <b-button
                    v-b-toggle.change-teacher-password
                    variant="secondary"
                    >Change Password</b-button
                  >
                </b-form>
                <br />
                <b-collapse id="change-teacher-password" class="mt-2">
                  <b-card>
                    <b-form @submit="updatePassword">
                      <b-row v-for="item in passwordOptions" :key="item.key">
                        <b-col sm="6">
                          <label :for="`account-pass-input-${item.key}`"
                            ><b>{{ item.label }}:</b></label
                          >
                        </b-col>
                        <b-col sm="6">
                          <b-input
                            :id="`account-pass-input-${item.key}`"
                            v-model="passwordForm[item.key]"
                            required
                          ></b-input
                          ><br />
                        </b-col>
                      </b-row>
                      <b-button type="submit" variant="primary"
                        >Set Password</b-button
                      >
                    </b-form>
                  </b-card>
                </b-collapse>
              </b-collapse>

              <b-collapse
                :visible="sectionTitle === 'Climate'"
                id="climate-settings-collapse"
              >
                <DeviceViewer />
              </b-collapse>

              <b-collapse
                :visible="sectionTitle === 'Device'"
                id="device-settings-collapse"
              >
                <b-form inline @submit="updateDevice">
                  <label>Device Name: </label
                  ><b-input
                    v-model="deviceInput"
                    :placeholder="currentDevice.name"
                    style="margin-left: 1rem;"
                    required
                  ></b-input>
                  <b-button type="submit" variant="primary">Update</b-button>
                  <b-button v-b-toggle.add-new-device variant="secondary"
                    >Register another device</b-button
                  >
                </b-form>
                <b-collapse id="add-new-device" class="mt-2">
                  <b-card>
                    <b-form @submit="registerDevice">
                      <b-row v-for="item in deviceOptions" :key="item.key">
                        <b-col sm="6">
                          <label :for="`device-registration-${item.key}`"
                            ><b>{{ item.label }}</b></label
                          >
                        </b-col>
                        <b-col sm="6">
                          <b-input
                            :id="`device-registration-${item.key}`"
                            v-model="deviceForm[item.key]"
                            required
                          ></b-input
                          ><br />
                        </b-col>
                      </b-row>
                      <b-button type="submit" variant="primary"
                        >Register</b-button
                      >
                    </b-form>
                  </b-card>
                </b-collapse>
              </b-collapse>
            </b-container>
          </b-jumbotron>
        </b-col>
      </b-row>
    </div>
  </div>
</template>

<script>
import NavBar from "../components/NavBar";
import api from "../api/index.js";
import TableHeaders from "../constants/TableHeaders.ts";
import CreatorOptions from "../constants/CreatorOptions.ts";
import DeviceViewer from "../components/DeviceViewer";
export default {
  name: "Settings",
  components: { NavBar, DeviceViewer },
  data() {
    return {
      currentDevice: null,
      devices: [],
      updateAlert: 0,
      updateMessage: "",
      sectionTitle: "",
      headers: TableHeaders.settingsButtons,
      options: [
        { option: "account", label: "Account" },
        { option: "climate", label: "Climate" },
        { option: "device", label: "Device" }
      ],
      teacherOptions: CreatorOptions.teacherAccount.options,
      teacherForm: {},
      passwordOptions: CreatorOptions.teacherPassword.options,
      passwordForm: { oldPass: "", newPass: "", repeatNewPass: "" },
      deviceOptions: CreatorOptions.deviceRegistration.options,
      deviceInput: "",
      deviceForm: { fopd_id: "", name: "" }
    };
  },
  beforeMount() {
    this.devices = api.getDevices();
    this.currentDevice = this.devices[0];
    this.teacherForm = this.$store.state.currentUser;
  },
  computed: {
    formatDevices() {
      let rows = this.devices.map(item => {
        let tmp = {};
        tmp.text = item.name;
        tmp.value = item;
        return tmp;
      });
      return rows;
    }
  },
  methods: {
    onSubmit(evt) {
      evt.preventDefault();
      this.$store.state.device = this.currentDevice;
    },
    resetAlert() {
      this.updateAlert = 0;
    },
    onRowSelected(items) {
      this.sectionTitle = items[0].label;
    },
    updateAccount(evt) {
      evt.preventDefault();
      this.updateMessage = "Account updated!";
      this.updateAlert = 3;
      api.updateTeacherName(this.teacherForm);
    },
    checkNewPass() {
      if (this.passwordForm.newPass !== this.passwordForm.repeatNewPass) {
        throw "New passwords do not match";
      }
    },
    updateDevice(evt) {
      evt.preventDefault();
      this.updateMessage = "Device name updated!";
      this.updateAlert = 3;
      api.updateDeviceName(this.deviceInput);
      this.devices = api.getDevices();
    },
    registerDevice(evt) {
      evt.preventDefault();
      try {
        api.registerDevice(this.deviceForm);
      } catch (e) {
        alert(e);
      }
      this.updateMessage = "Device registered!";
      this.updateAlert = 3;
      this.devices = api.getDevices();
    },
    updatePassword(evt) {
      evt.preventDefault();
      try {
        this.checkNewPass();
        api.changeTeacherPassword(
          this.passwordForm.oldPass,
          this.passwordForm.newPass
        );
      } catch (e) {
        alert(e);
        return;
      }
      this.updateMessage = "Password changed!";
      this.updateAlert = 3;
    }
  }
};
</script>

<style>
.center {
  margin: auto;
  width: 60%;
  padding: 10px;
}
</style>
