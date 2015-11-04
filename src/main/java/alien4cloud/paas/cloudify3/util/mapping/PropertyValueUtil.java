package alien4cloud.paas.cloudify3.util.mapping;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;

import lombok.extern.slf4j.Slf4j;
import alien4cloud.model.components.AbstractPropertyValue;
import alien4cloud.model.components.ComplexPropertyValue;
import alien4cloud.model.components.ListPropertyValue;
import alien4cloud.model.components.PropertyValue;
import alien4cloud.model.components.ScalarPropertyValue;
import alien4cloud.paas.cloudify3.error.PropertyValueMappingException;
import alien4cloud.utils.services.PropertyValueService;

import com.google.common.collect.Lists;
import com.google.common.collect.Maps;

/**
 * Simple utility that deep
 */
@Slf4j
public final class PropertyValueUtil {

    /**
     * Map properties of a template from tosca to cloudify properties.
     *
     * @param allTypesPropertiesMappings Properties mapping for all tosca element in the topology
     * @param nodeType Tosca elementType of the template for which to map properties
     * @param properties The properties to map
     * @return A map of mapped properties
     */
    public static Map<String, AbstractPropertyValue> mapProperties(Map<String, Map<String, IPropertyMapping>> allTypesPropertiesMappings, String nodeType,
            Map<String, AbstractPropertyValue> properties) {

        if (allTypesPropertiesMappings == null || allTypesPropertiesMappings.isEmpty()) {
            // do not change prop map
            return properties;
        }

        // first of all get the mapping for the node type
        Map<String, IPropertyMapping> typePropertiesMappings = allTypesPropertiesMappings.get(nodeType);
        return mapProperties(allTypesPropertiesMappings, typePropertiesMappings, properties);
    }

    /**
     * Map properties of a template from tosca to cloudify properties.
     *
     * @param typePropertiesMappings Properties mapping for the tosca element related to the template
     * @param properties The properties to map
     * @return A map of mapped properties
     */
    public static Map<String, AbstractPropertyValue> mapProperties(Map<String, IPropertyMapping> typePropertiesMappings,
            Map<String, AbstractPropertyValue> properties) {
        Map<String, Map<String, IPropertyMapping>> allTypesPropertiesMappings = Maps.newHashMap();
        return mapProperties(allTypesPropertiesMappings, typePropertiesMappings, properties);
    }

    /**
     * Map properties of a template from tosca to cloudify properties.
     *
     * @param allTypesPropertiesMappings Properties mapping for all tosca element in the topology
     * @param typePropertiesMappings Properties mapping for the tosca element related to the template
     * @param properties The properties to map
     * @return A map of mapped properties
     */
    private static Map<String, AbstractPropertyValue> mapProperties(Map<String, Map<String, IPropertyMapping>> allTypesPropertiesMappings,
            Map<String, IPropertyMapping> typePropertiesMappings, Map<String, AbstractPropertyValue> properties) {
        if (typePropertiesMappings == null || typePropertiesMappings.isEmpty()) {
            // do not change prop map
            return properties;
        }

        Map<String, AbstractPropertyValue> mappedProperties = Maps.newHashMap();
        for (Map.Entry<String, AbstractPropertyValue> propertyEntry : properties.entrySet()) {
            PropertyValue sourcePropertyValue = (PropertyValue) propertyEntry.getValue();
            if (sourcePropertyValue == null) {
                continue;
            }
            mapProperty(allTypesPropertiesMappings, typePropertiesMappings, propertyEntry.getKey(), sourcePropertyValue, mappedProperties);
        }
        return mappedProperties;
    }

    private static void mapProperty(Map<String, Map<String, IPropertyMapping>> allTypesPropertiesMappings,
            Map<String, IPropertyMapping> typesPropertiesMappings, String propertyName, PropertyValue sourcePropertyValue,
            Map<String, AbstractPropertyValue> mappedProperties) {

        IPropertyMapping mapping = typesPropertiesMappings.get(propertyName);
        if (mapping == null) {
            // if the property is not mapped, just keep it as is.
            mergeAndAddMappedProperty(propertyName, sourcePropertyValue, mappedProperties);
        } else if (mapping instanceof PropertyMapping) {
            processPropertyMapping(allTypesPropertiesMappings, (PropertyMapping) mapping, propertyName, sourcePropertyValue, mappedProperties);
        } else if (mapping instanceof ComplexPropertyMapping) {
            processComplexPropertyMapping(allTypesPropertiesMappings, propertyName, sourcePropertyValue, mappedProperties, mapping);
        }

    }

    private static void processComplexPropertyMapping(Map<String, Map<String, IPropertyMapping>> allTypesPropertiesMappings, String propertyName,
            PropertyValue sourcePropertyValue, Map<String, AbstractPropertyValue> mappedProperties, IPropertyMapping mapping) {
        ComplexPropertyMapping complexPropertyMapping = (ComplexPropertyMapping) mapping;
        String complexPropertyType = complexPropertyMapping.getType();
        if (complexPropertyType == null) {
            log.warn(String.format("The property '%s' is known as a complex property mapping but the type isn't defined, ignore the mapping !",
                    propertyName));
            return;
        }
        // get the mapping for this type
        Map<String, IPropertyMapping> typeMapping = allTypesPropertiesMappings.get(complexPropertyType);
        if (typeMapping == null) {
            log.warn(String.format(
                    "The property '%s' is known as a complex property mapping but the mapping for the type '%s' can not be found, ignore the mapping !",
                    propertyName, complexPropertyType));
            return;
        }
        if (complexPropertyMapping.isList()) {
            // the mapping concerns a list
            if (!(sourcePropertyValue instanceof ListPropertyValue)) {
                // the property value is not a list, ignore and log
                log.warn(String.format("The property '%s' should be a list but is not, ignore the mapping !", propertyName));
                return;
            }
            ListPropertyValue listPropertyValue = (ListPropertyValue) sourcePropertyValue;
            ListPropertyValue targetListPropertyValue = new ListPropertyValue(new ArrayList<Object>());
            for (Object listItem : listPropertyValue.getValue()) {
                if (!(listItem instanceof ComplexPropertyValue)) {
                    // the item is not a complex property, ignore and log
                    log.warn(String.format("The property '%s' list item should be a complex property but is not, ignore the mapping !", propertyName));
                    continue;
                }
                ComplexPropertyValue complexPropertyValue = (ComplexPropertyValue) listItem;
                // for each item we build a map
                Map<String, AbstractPropertyValue> itemProperties = Maps.newHashMap();
                for (Entry<String, Object> complexPropertyEntry : complexPropertyValue.getValue().entrySet()) {
                    PropertyValue complexPropertyEntryValue = propertyValueFromObject(complexPropertyEntry.getValue());
                    String complexPropertyEntryName = complexPropertyEntry.getKey();
                    mapProperty(allTypesPropertiesMappings, typeMapping, complexPropertyEntryName, complexPropertyEntryValue, itemProperties);
                }
                targetListPropertyValue.getValue().add(itemProperties);
            }
            // TODO: add the ability to change to taget property name ?
            mappedProperties.put(propertyName, targetListPropertyValue);
        } else {
            // this a mapped complex type but not a list
            if (!(sourcePropertyValue instanceof ComplexPropertyValue)) {
                // the item is not a complex property, ignore and log
                log.warn(String.format("The property '%s' should be a complex property but is not, ignore the mapping !", propertyName));
                return;
            }
            ComplexPropertyValue complexPropertyValue = (ComplexPropertyValue) sourcePropertyValue;
            Map<String, AbstractPropertyValue> itemProperties = Maps.newHashMap();
            for (Entry<String, Object> complexPropertyEntry : complexPropertyValue.getValue().entrySet()) {
                PropertyValue complexPropertyEntryValue = propertyValueFromObject(complexPropertyEntry.getValue());
                String complexPropertyEntryName = complexPropertyEntry.getKey();
                mapProperty(allTypesPropertiesMappings, typeMapping, complexPropertyEntryName, complexPropertyEntryValue, itemProperties);
            }
            mappedProperties.put(propertyName, propertyValueFromObject(itemProperties));
        }
    }

    private static void processPropertyMapping(Map<String, Map<String, IPropertyMapping>> propertyMappings, PropertyMapping mapping, String propertyName,
            PropertyValue sourcePropertyValue, Map<String, AbstractPropertyValue> mappedProperties) {

        if (mapping == null || mapping.getSubMappings().size() == 0) {
            // if the property is not mapped, just keep it as is.
            mergeAndAddMappedProperty(propertyName, sourcePropertyValue, mappedProperties);
        } else {
            // if the property is mapped then apply the mapping.
            for (PropertySubMapping subMapping : mapping.getSubMappings()) {
                String sourcePath = subMapping.getSourceMapping().getPath();
                TargetMapping targetMapping = subMapping.getTargetMapping();

                if (targetMapping.getProperty() == null) {
                    continue; // skip this property
                }

                Object sourceValue = PropertyValueService.getValue(sourcePropertyValue.getValue(), sourcePath);
                // if there is a specified unit, convert the value to the expected unit.
                if (targetMapping.getUnit() != null) {
                    // need the property type to IComparablePropertyType
                    sourceValue = PropertyValueService.getValueInUnit(sourceValue, targetMapping.getUnit(), subMapping.getSourceMapping()
                            .getPropertyDefinition());
                }

                if (targetMapping.getPath() == null) {
                    // set the property with the value
                    mergeAndAddMappedProperty(targetMapping.getProperty(), propertyValueFromObject(sourceValue), mappedProperties);
                } else {
                    // extract the value
                    PropertyValue targetProperty = (PropertyValue) mappedProperties.get(targetMapping.getProperty());
                    Object targetValue = sourceValue;
                    if (targetProperty != null) {
                        targetValue = PropertyValueService.getValue(targetProperty.getValue(), targetMapping.getPath());
                        targetValue = merge(sourceValue, targetValue);
                    } else {
                        targetProperty = propertyValueFromObject(new HashMap<>());
                        mappedProperties.put(targetMapping.getProperty(), targetProperty);
                    }
                    // set the value
                    setValue(targetProperty.getValue(), targetMapping.getPath(), targetValue);
                }
            }
        }
    }

    private static void mergeAndAddMappedProperty(String propertyName, PropertyValue sourcePropertyValue, Map<String, AbstractPropertyValue> mappedProperties) {
        PropertyValue mappedProperty = (PropertyValue) mappedProperties.get(propertyName);
        if (sourcePropertyValue.getValue() != null) {
            mappedProperty = PropertyValueUtil.merge(sourcePropertyValue, mappedProperty);
        }
        if (mappedProperty != null) {
            mappedProperties.put(propertyName, mappedProperty);
        }
    }

    /**
     * Map properties from tosca to cloudify properties.
     *
     * @param propMappings The property mappings
     * @param properties The properties to map.
     */
    @Deprecated
    public static Map<String, AbstractPropertyValue> _mapProperties(Map<String, PropertyMapping> propMappings, Map<String, AbstractPropertyValue> properties) {
        if (propMappings == null || propMappings.isEmpty()) {
            // do not change prop map
            return properties;
        }

        Map<String, AbstractPropertyValue> mappedProperties = Maps.newHashMap();

        for (Map.Entry<String, AbstractPropertyValue> propertyEntry : properties.entrySet()) {
            PropertyValue sourcePropertyValue = (PropertyValue) propertyEntry.getValue();

            PropertyMapping mapping = propMappings.get(propertyEntry.getKey());

            if (sourcePropertyValue == null) {
                continue;
            }

            if (mapping == null || mapping.getSubMappings().size() == 0) {
                // if the property is not mapped, just keep it as is.
                // mergeAndAddMappedProperty(propertyEntry.getKey(), sourcePropertyValue, mappedProperties);
                PropertyValue mappedProperty = PropertyValueUtil.merge(sourcePropertyValue, (PropertyValue) mappedProperties.get(propertyEntry.getKey()));
                mappedProperties.put(propertyEntry.getKey(), mappedProperty);
            } else {
                // if the property is mapped then apply the mapping.
                for (PropertySubMapping subMapping : mapping.getSubMappings()) {
                    String sourcePath = subMapping.getSourceMapping().getPath();
                    TargetMapping targetMapping = subMapping.getTargetMapping();

                    if (targetMapping.getProperty() == null) {
                        continue; // skip this property
                    }

                    Object sourceValue = PropertyValueService.getValue(sourcePropertyValue.getValue(), sourcePath);
                    // if there is a specified unit, convert the value to the expected unit.
                    if (targetMapping.getUnit() != null) {
                        // need the property type to IComparablePropertyType
                        sourceValue = PropertyValueService.getValueInUnit(sourceValue, targetMapping.getUnit(), subMapping.getSourceMapping()
                                .getPropertyDefinition());
                    }

                    PropertyValue targetProperty = (PropertyValue) mappedProperties.get(targetMapping.getProperty());
                    if (targetMapping.getPath() == null) {
                        // set the property with the value
                        PropertyValue mappedProperty = PropertyValueUtil.merge(propertyValueFromObject(sourceValue), targetProperty);
                        mappedProperties.put(targetMapping.getProperty(), mappedProperty);
                    } else {
                        // extract the value
                        Object targetValue = sourceValue;
                        if (targetProperty != null) {
                            targetValue = PropertyValueService.getValue(targetProperty.getValue(), targetMapping.getPath());
                            targetValue = merge(sourceValue, targetValue);
                        } else {
                            targetProperty = propertyValueFromObject(new HashMap<>());
                            mappedProperties.put(targetMapping.getProperty(), targetProperty);
                        }
                        // set the value
                        setValue(targetProperty.getValue(), targetMapping.getPath(), targetValue);
                    }
                }
            }
        }

        return mappedProperties;
    }

    /**
     * Return a property value based on the type of an object.
     *
     * @param object The object to wrap into a PropertyValue.
     * @return A property value that wraps the given object.
     */
    private static PropertyValue propertyValueFromObject(Object object) {
        if (object instanceof PropertyValue) {
            return (PropertyValue) object;
        } else if (object instanceof Map) {
            return new ComplexPropertyValue((Map<String, Object>) object);
        } else if (object instanceof List) {
            return new ListPropertyValue((List<Object>) object);
        } else {
            return new ScalarPropertyValue((String) object);
        }
    }

    /**
     * Merge a source property value into a target property. If target is not null, the source is merged directly in the target object and the target object is
     * returned.
     *
     * @param source The source property value.
     * @param target The target property value.
     * @return The merged object.
     */
    public static PropertyValue merge(PropertyValue source, PropertyValue target) {
        if (source == null) {
            return target;
        }
        if (target == null) {
            return deepClone(source);
        }
        // perform the property merge.
        Object clonedSource = deepClone(source.getValue());
        // merge the clonedSource into the target value
        target.setValue(merge(clonedSource, target.getValue()));
        return target;
    }

    private static Object merge(Object sourcePropertyValueObject, Object targetPropertyValueObject) {
        if (targetPropertyValueObject == null) {
            return sourcePropertyValueObject;
        }
        if (sourcePropertyValueObject instanceof Map && targetPropertyValueObject instanceof Map) {
            Map result = Maps.newHashMap((Map) targetPropertyValueObject);
            result.putAll((Map) sourcePropertyValueObject);
            return result;
        } else {
            return sourcePropertyValueObject;
        }
    }

    private static void setValue(Object target, String path, Object value) {
        String[] pathElements = path.split("\\.");
        Object current = target;
        for (int i = 0; i < pathElements.length - 1; i++) {
            String pathElement = pathElements[i];
            if (current instanceof Map) {
                current = ((Map) current).get(pathElement);
            } else {
                throw new PropertyValueMappingException("Expected a map");
            }
        }
        if (current instanceof Map) {
            // target should be a map
            ((Map) current).put(pathElements[pathElements.length - 1], value);
        } else {
            throw new PropertyValueMappingException("Expected a map");
        }
    }

    /**
     * Simple utility that deep clones an object made of Map, List and String.
     *
     * @param propertyValue The property value to clone.
     */
    public static PropertyValue deepClone(PropertyValue propertyValue) {
        if (propertyValue instanceof ListPropertyValue) {
            return new ListPropertyValue(deepClone(((ListPropertyValue) propertyValue).getValue()));
        } else if (propertyValue instanceof ComplexPropertyValue) {
            return new ComplexPropertyValue(deepClone(((ComplexPropertyValue) propertyValue).getValue()));
        }
        // must be a scalar property value
        return new ScalarPropertyValue(((ScalarPropertyValue) propertyValue).getValue());
    }

    /**
     * Deep clone an object that compose a property value (every element is a String, a Map or a List).
     *
     * @param propertyValueObject The object to clone.
     * @return A clone of the property value object.
     */
    private static <T> T deepClone(T propertyValueObject) {
        T clone;
        if (propertyValueObject instanceof Map) {
            Map map = Maps.newHashMap();
            Map<String, ?> propertyValueObjectMap = (Map) propertyValueObject;
            for (Map.Entry<String, ?> entry : propertyValueObjectMap.entrySet()) {
                // key is a string in property values structure
                map.put(entry.getKey(), deepClone(entry.getValue()));
            }
            clone = (T) map;
        } else if (propertyValueObject instanceof List) {
            List list = Lists.newArrayList();
            for (Object element : ((List) propertyValueObject)) {
                list.add(deepClone(element));
            }
            clone = (T) list;
        } else if (propertyValueObject instanceof String) {
            clone = propertyValueObject;
        } else {
            log.warn("Property deep clone is just making a simple copy for type {} and value {}. Expecting a String for these situations.", propertyValueObject
                    .getClass().getName(), propertyValueObject);
            clone = propertyValueObject;
        }

        return clone;
    }
}