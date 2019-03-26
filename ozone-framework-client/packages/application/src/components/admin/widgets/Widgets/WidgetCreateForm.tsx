import * as React from "react";
import { Form, Formik, FormikActions, FormikProps } from "formik";
import { array, boolean, number, object, string } from "yup";

import { WidgetCreateRequest } from "../../../../api/models/WidgetDTO";
import { CancelButton, CheckBox, FormError, HiddenField, SelectField, SubmitButton, TextField } from "../../../form";

import * as uuidv4 from "uuid/v4";

import * as styles from "../Widgets.scss";

import { WidgetTypeReference } from "../../../../api/models/WidgetTypeDTO";
import { MenuItem } from "@blueprintjs/core";
import { ItemRenderer } from "@blueprintjs/select";

interface WidgetCreateProps {
    onSubmit: (data: WidgetCreateRequest) => Promise<boolean>;
    onCancel: () => void;
    items: WidgetTypeReference[];
}

const WidgetTypeSelect = SelectField.ofType<WidgetTypeReference>();

const renderWidgetType: ItemRenderer<WidgetTypeReference> = (
    widgetType: WidgetTypeReference,
    { handleClick, modifiers }
) => {
    return <MenuItem key={widgetType.name} onClick={handleClick} text={widgetType.name} />;
};

export const WidgetCreateForm: React.FunctionComponent<WidgetCreateProps> = ({ onSubmit, onCancel, items }) => (
    <Formik
        initialValues={{
            displayName: "",
            widgetVersion: "",
            description: "",
            widgetUrl: "",
            imageUrlSmall: "",
            imageUrlMedium: "",
            width: 200,
            height: 200,
            widgetGuid: uuidv4.default(),
            universalName: "",
            visible: true,
            background: false,
            singleton: false,
            mobileReady: false,
            widgetTypes: [],
            title: ""
        }}
        validationSchema={CreateWidgetSchema}
        onSubmit={async (values: WidgetCreateRequest, actions: FormikActions<WidgetCreateRequest>) => {
            values.height = Number(values.height);
            values.width = Number(values.width);

            const isSuccess = await onSubmit(values);
            actions.setStatus(isSuccess ? null : { error: "An unexpected error has occurred" });
            actions.setSubmitting(false);
        }}
    >
        {(formik: FormikProps<WidgetCreateRequest>) => (
            <div data-element-id="widget-admin-widget-create-form">
                <Form className={styles.form}>
                    <div>
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="displayName"
                            label="Name"
                            placeholder="MyAppComponent"
                        />
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="description"
                            label="Description"
                            placeholder="Describe the App Component"
                        />
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="widgetVersion"
                            label="Version"
                            placeholder="1.0"
                        />
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="universalName"
                            label="Universal Name"
                            placeholder="MyAppComponent.mycompany.com"
                        />

                        <HiddenField
                            inline={true}
                            className={styles.inline_form_label}
                            name="widgetGuid"
                            label="GUID"
                        />

                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="widgetUrl"
                            label="URL"
                            placeholder="https://mycompany.com/appcomponent/MyAppComponent.html"
                        />
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="imageUrlSmall"
                            label="Small Icon URL"
                            placeholder="https://mycompany.com/appcomponent/images/containerIcon.png"
                        />
                        <TextField
                            inline={true}
                            className={styles.inline_form_label}
                            name="imageUrlMedium"
                            label="Medium Icon URL"
                            placeholder="https://mycompany.com/appcomponent/images/launchMenuIcon.png"
                        />

                        <TextField inline={true} className={styles.inline_form_label} name="width" label="Width" />
                        <TextField inline={true} className={styles.inline_form_label} name="height" label="Height" />

                        <WidgetTypeSelect
                            inline={true}
                            className={styles.inline_form_label}
                            name="widgetType"
                            label="Widget Type"
                            items={items}
                            itemRenderer={renderWidgetType}
                            extractLabel={(item: WidgetTypeReference) => item.name}
                            onSelectItem={(widgetType: WidgetTypeReference) => {
                                formik.values.widgetTypes = [widgetType];
                                formik.validateForm();
                            }}
                        />

                        <CheckBox
                            inline={true}
                            className={styles.inline_form_label}
                            name="singleton"
                            label="Singleton"
                        />
                        <CheckBox
                            inline={true}
                            className={styles.inline_form_label}
                            name="mobileReady"
                            label="Mobile Ready"
                        />
                        <CheckBox inline={true} className={styles.inline_form_label} name="visible" label="Visible" />
                        <CheckBox
                            inline={true}
                            className={styles.inline_form_label}
                            name="background"
                            label="Background"
                        />

                        {formik.status && formik.status.error && <FormError message={formik.status.error} />}
                    </div>

                    <div className={styles.buttonBar} data-element-id="widget-admin-widget-create-submit-button">
                        <CancelButton className={styles.cancelButton} onClick={onCancel} />
                        <SubmitButton className={styles.submitButton} />
                    </div>
                </Form>
            </div>
        )}
    </Formik>
);

const CreateWidgetSchema = object().shape({
    displayName: string().required("Required"),
    widgetUrl: string().required("Required"),
    widgetVersion: string(),
    description: string(),
    imageUrlSmall: string().required("Required"),
    imageUrlMedium: string().required("Required"),
    width: number()
        .integer("Must be an integer")
        .min(200)
        .required("Required"),
    height: number()
        .integer("Must be an integer")
        .min(200)
        .required("Required"),
    widgetGuid: string(),
    universalName: string(),
    visible: boolean(),
    background: boolean(),
    singleton: boolean(),
    mobileReady: boolean(),
    widgetTypes: array().required("Required")
});